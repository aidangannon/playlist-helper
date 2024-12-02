import json


def lambda_handler(event, context):
    key_words = event['queryStringParameters']['keyWords']

    print(len(key_words))
    for word in key_words:
        print(word)

    return {
        'statusCode': 200,
        'body': json.dumps({
            'message': 'this is a test'
        })
    }
