import json
import app


def lambda_handler(event=None, context=None):
    response = app.predict("report.txt")
    print(response)
    return {
        'statusCode': 200,
        'body': json.dumps(response)
    }
