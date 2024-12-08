import base64
import json
import os

import boto3
from botocore.exceptions import ClientError

BUCKET_NAME = 'S3_BUCKET_NAME'

S3 = boto3.client('s3')
Username = str
Password = str


def lambda_handler(event, context):
    S3.put_object(Bucket=os.environ['S3_BUCKET_NAME'],
                                Key='users/admin',
                                Body=json.dumps({"password": event['queryStringParameters']['password']}),
                                ContentType="application/json")

    print(f"EVENT: {event}")
    print(f"CONTEXT: {context}")
    does_header_exist, username, password = get_username_and_password(event)

    if not does_header_exist:
        print("Authorization header missing")
        return {
            'statusCode': 401,
            'body': json.dumps({
                'message': f'Unauthorized'
            })
        }

    does_user_exist, admin = get_user(username)

    if not does_user_exist:
        print("User does not exist")
        return {
            'statusCode': 401,
            'body': json.dumps({
                'message': f'Unauthorized'
            })
        }

    if admin['password'] != password:
        print("Password is invalid")
        return {
            'statusCode': 401,
            'body': json.dumps({
                'message': f'Unauthorized'
            })
        }

    if not 'queryStringParameters' in event:
        return {
            'statusCode': 400,
            'body': json.dumps({
                'message': 'keyWords parameter is required'
            })
        }

    if not 'keyWords' in event['queryStringParameters']:
        return {
            'statusCode': 400,
            'body': json.dumps({
                'message': 'keyWords parameter is required'
            })
        }

    key_words_array = event['queryStringParameters']['keyWords'].split(',')

    print(f'key words {key_words_array}')

    return {
        'statusCode': 200,
        'body': json.dumps({
            'message': 'this is a test'
        })
    }


def get_user(username) -> (bool, dict):
    try:
        admin = S3.get_object(Bucket=os.environ[BUCKET_NAME],
                              Key=f'users/{username}')['Body'].read()
        return True, admin
    except ClientError:
        return False, {}


def get_username_and_password(event) -> (bool, Username, Password):
    authorization_header = event.get('headers', {}).get('authorization')
    header_not_found_response = (False, None, None)
    if not authorization_header:
        return header_not_found_response
    if not authorization_header.startswith("Basic "):
        return header_not_found_response

    basic_key = authorization_header.split(" ")[1]
    decoded_credentials = base64.b64decode(basic_key).decode('utf-8')
    print(f"decoded auth key {decoded_credentials}")
    username, password = decoded_credentials.split(":", 1)
    return True, username, password
