import json


def lambda_handler(event, context):
    key_words_array = event['queryStringParameters']['keyWords'].split(',')

    print(len(key_words_array))
    for word in key_words_array:
        print(word)

    return {
        'statusCode': 200,
        'body': json.dumps({
            'message': 'this is a test'
        })
    }
