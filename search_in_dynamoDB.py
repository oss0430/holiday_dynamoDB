import json
import boto3


def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    query_parameters = event.get('queryStringParameters')
    query_date = query_parameters['date']
    print(query_date)
    
    return_key = 0
    holiday_info = {
        
    }
    client = boto3.client('dynamodb')
    for i in range (31):
        if(i<10):
            date = str(query_date)+ "0" + str(i)
        else:
            date = str(query_date) + str(i)
        print(date)
        response = client.batch_get_item(
            RequestItems = {
                'Holiday' : {
                    'Keys' : [
                        {
                            'sortdate' : {
                                'N' : date
                            }
                        }
                    ]
                }
            }
        )
        temp = response['Responses'].get('Holiday')
        
        if not temp:
            print("list1 is empty")
        
        if temp:
            print(temp)
            holiday_info.setdefault(return_key,temp)
            return_key += 1

        

    return {
        'statusCode' : 200,
        'body' : json.dumps(holiday_info)
    }

'''
Test Event Name
test

Response
{
  "statusCode": 200,
  "body": "{\"Responses\": {\"Holiday\": [{\"holiday\": {\"S\": \"\\uac1c\\ucc9c\\uc808\"}, \"date\": {\"N\": \"2210\"}, \"sortdate\": {\"N\": \"221003\"}}]}, \"UnprocessedKeys\": {}, \"ResponseMetadata\": {\"RequestId\": \"JRQ9IELPKGGFQGB3LP731BA1SFVV4KQNSO5AEMVJF66Q9ASUAAJG\", \"HTTPStatusCode\": 200, \"HTTPHeaders\": {\"server\": \"Server\", \"date\": \"Tue, 15 Nov 2022 14:03:23 GMT\", \"content-type\": \"application/x-amz-json-1.0\", \"content-length\": \"124\", \"connection\": \"keep-alive\", \"x-amzn-requestid\": \"JRQ9IELPKGGFQGB3LP731BA1SFVV4KQNSO5AEMVJF66Q9ASUAAJG\", \"x-amz-crc32\": \"178670077\"}, \"RetryAttempts\": 0}}"
}

Function Logs
START RequestId: 8196a990-7309-4ded-97c6-e236c49ebcde Version: $LATEST
221000
list1 is empty
221001
list1 is empty
221002
list1 is empty
221003
[{'holiday': {'S': '개천절'}, 'date': {'N': '2210'}, 'sortdate': {'N': '221003'}}]
END RequestId: 8196a990-7309-4ded-97c6-e236c49ebcde
REPORT RequestId: 8196a990-7309-4ded-97c6-e236c49ebcde	Duration: 1476.14 ms	Billed Duration: 1477 ms	Memory Size: 128 MB	Max Memory Used: 66 MB	Init Duration: 251.00 ms

Request ID
8196a990-7309-4ded-97c6-e236c49ebcde
'''