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
                            'date' : {
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