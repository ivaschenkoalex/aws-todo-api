import json
import os
import time

import boto3
from aws_lambda_powertools import Logger, Tracer

# Structured JSON logging & tracing
logger = Logger(service="todo-api")
tracer = Tracer(service="todo-api")

table = boto3.resource("dynamodb").Table(os.environ["TABLE_NAME"])


def resp(code, body):
    return {
        "statusCode": code,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(body),
    }


@tracer.capture_lambda_handler  # X-Ray: wrap the handler
@logger.inject_lambda_context(log_event=True)  # logs context and (optionally) the event
def handler(event, context):
    # Works with HTTP API (preferred) or REST API events
    http_ctx = (event.get("requestContext") or {}).get("http") or {}
    method = http_ctx.get("method") or event.get("httpMethod", "GET")

    logger.append_keys(method=method)  # include method in all subsequent log lines

    if method == "POST":
        try:
            body = json.loads(event.get("body") or "{}")
        except json.JSONDecodeError:
            logger.warning("invalid_json_body")
            return resp(400, {"error": "invalid JSON"})

        item_id = str(int(time.time() * 1000))
        item = {"id": item_id, "payload": body}

        # Trace the DynamoDB write as a subsegment
        with tracer.provider.in_subsegment("dynamodb_put"):
            table.put_item(Item=item)

        logger.info("todo_created", extra={"id": item_id})
        return resp(201, {"id": item_id})

    if method == "GET":
        qp = event.get("queryStringParameters") or {}
        path_params = event.get("pathParameters") or {}
        item_id = qp.get("id") or path_params.get("id")
        if not item_id:
            logger.warning("missing_id")
            return resp(400, {"error": "id required"})

        # Trace the DynamoDB read as a subsegment
        with tracer.provider.in_subsegment("dynamodb_get"):
            r = table.get_item(Key={"id": item_id})

        found = "yes" if "Item" in r else "no"
        logger.info("todo_read", extra={"id": item_id, "found": found})
        return resp(200, r.get("Item") or {})

    logger.info("method_ok_but_not_implemented")
    return resp(200, {"ok": True, "method": method})
