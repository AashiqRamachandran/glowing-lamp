import json
import app


def lambda_handler(event=None, context=None):
    body = event['body']

    response = app.predict(body)

    print(response)
    return {
        'statusCode': 200,
        'body': json.dumps(response)
    }
