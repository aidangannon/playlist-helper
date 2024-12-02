import json


def lambda_handler(event, context):

    key_words = event['queryStringParameters']['keyWords']

    return {
        'statusCode': 200,
        'body': json.dumps({
            'message': 'this is a test'
        })
    }
