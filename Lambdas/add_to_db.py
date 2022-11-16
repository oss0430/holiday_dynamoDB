import json
import boto3


def lambda_handler(event, context):
    
    body = event['body'].encode("utf8")
    body = body.decode('unicode_escape')
    body = body[1:-1]
    
    newdict = eval(body)
    
    items = {'date' : int(newdict['date']),
             'sortdate' : int(newdict['sortdate']),
             'holiday'  : newdict['holiday']}

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('Holidays')
    response = table.put_item(Item = items)
    
    return response