import json
import os

import boto3
from moto import mock_dynamodb

from lambda_function import handler


@mock_dynamodb
def test_post_then_get_roundtrip():
    os.environ["TABLE_NAME"] = "todo-dev"

    dynamodb = boto3.resource("dynamodb", region_name="us-east-1")
    dynamodb.create_table(
        TableName="todo-dev",
        KeySchema=[{"AttributeName": "id", "KeyType": "HASH"}],
        AttributeDefinitions=[{"AttributeName": "id", "AttributeType": "S"}],
        BillingMode="PAY_PER_REQUEST",
    )

    post_event = {
        "requestContext": {"http": {"method": "POST"}},
        "body": json.dumps({"task": "write tests"}),
    }
    post_resp = handler(post_event, {})
    assert post_resp["statusCode"] == 201
    new_id = json.loads(post_resp["body"])["id"]

    get_event = {
        "requestContext": {"http": {"method": "GET"}},
        "queryStringParameters": {"id": new_id},
    }
    get_resp = handler(get_event, {})
    assert get_resp["statusCode"] == 200
    obj = json.loads(get_resp["body"])
    assert obj["id"] == new_id
    assert obj["payload"]["task"] == "write tests"
