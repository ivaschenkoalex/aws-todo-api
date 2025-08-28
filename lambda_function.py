import os, json, time, boto3
table = boto3.resource('dynamodb').Table(os.environ['TABLE_NAME'])

def resp(code, body):
    return {"statusCode": code, "headers": {"Content-Type":"application/json"},
            "body": json.dumps(body)}

def handler(event, context):
    # Works with HTTP API (preferred) or REST API events
    method = (event.get("requestContext", {}).get("http", {}) or {}).get("method") \
             or event.get("httpMethod", "GET")

    if method == "POST":
        body = json.loads(event.get("body") or "{}")
        item_id = str(int(time.time()*1000))
        item = {"id": item_id, "payload": body}
        table.put_item(Item=item)
        return resp(201, {"id": item_id})

    if method == "GET":
        qp = event.get("queryStringParameters") or {}
        path_params = event.get("pathParameters") or {}
        item_id = qp.get("id") or path_params.get("id")
        if not item_id: return resp(400, {"error":"id required"})
        r = table.get_item(Key={"id": item_id})
        return resp(200, r.get("Item") or {})

    return resp(200, {"ok": True, "method": method})

