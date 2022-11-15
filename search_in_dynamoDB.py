import json
import boto3

def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('User')
    query_parameters = event.get('queryStringParameters')
    print(query_parameters)
    #date = query_parameters.get('date')
    item = table.get_item(
        Key = {
            'no' : '1'
        }
    )
    print(item)
    
    
    return {
        'statusCode' : 200,
        'body' : json.dumps(item.get('Item'))
    }
