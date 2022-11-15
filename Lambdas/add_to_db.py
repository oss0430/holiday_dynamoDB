import json
import boto3

def lambda_handler(event, context):
    items = {'date' : int(event['date']),
             'sortdate' : int(event['sortdate']),
             'holiday'  : event['holiday']}

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('Holidays')
    response = table.put_item(Item = items)
    
    return response
