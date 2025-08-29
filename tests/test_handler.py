import os
import json
from moto import mock_dynamodb
import boto3

# Import from the lambda file in repo root
from lambda_function import handler

@mock_dynamodb
def test_post_then_get_roundtrip():
    # Set env var for the function
    os.environ["TABLE_NAME"] = "todo-dev"

    # Create a mock DynamoDB table
    dynamodb = boto3.resource("dynamodb", region_name="us-east-2")
    dynamodb.create_table(
        TableName="todo-dev",
        KeySchema=[{"AttributeName": "id", "KeyType": "HASH"}],
        AttributeDefinitions=[{"AttributeName": "id", "AttributeType": "S"}],
        BillingMode="PAY_PER_REQUEST",
    )

    # Simulate POST /todo
    post_event = {
        "requestContext": {"http": {"method": "POST"}},
        "body": json.dumps({"task": "write tests"})
    }
    post_resp = handler(post_event, {})
    assert post_resp["statusCode"] == 201
    new_id = json.loads(post_resp["body"])["id"]
    assert new_id

    # Simulate GET /todo?id=<new_id>
    get_event = {
        "requestContext": {"http": {"method": "GET"}},
        "queryStringParameters": {"id": new_id}
    }
    get_resp = handler(get_event, {})
    assert get_resp["statusCode"] == 200
    obj = json.loads(get_resp["body"])
    assert obj["id"] == new_id
    assert obj["payload"]["task"] == "write tests"
