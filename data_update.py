import requests
import json 
from urllib.parse import urlencode

class DataUpdater():
    def __init__(
        self,
        key = None,
        url = None,
        aws_url = None,
    )-> None:
        self.key = key
        self.url = url
        self.aws_url = aws_url
        return None
    
    def _make_get_request(
        self,
        solYear,
        solMonth
    )-> requests.models.Response :

        params ={'serviceKey' : self.key, 'solYear' : solYear, 'solMonth' : solMonth, '_type' : 'json'}
        response = requests.get(self.url, params=params)
        return response

    def _parse_response(
        self,
        response
    ) -> dict:
        json_response = json.loads(response.content)
        list_response = json_response["response"]["body"]["items"]["item"]
        if not isinstance(list_response, list):
            list_response = [list_response]
        parsed_list = []
        for dict in list_response:
            
            holiday_date = str(dict['locdate'])[2:]
            holiday_sortdate = str(dict['locdate'])[2:6]
            holiday_name = str(dict['dateName'])

            parsed_list.append({"date" : holiday_date,"sortdate" : holiday_sortdate,"holiday" : holiday_name})
        
        return parsed_list

    def load_public_api_with_json(
        self,
        file_path
    )-> None:
    
        with open(file_path, 'r') as file:
            data = json.load(file)
            self.key = data['key_decoding']
            self.url = data['url']    

        return None

    def load_aws_api_with_json(
        self,
        file_path
    )-> None:
    
        with open(file_path, 'r') as file:
            data = json.load(file)
            self.aws_url = data['url']    
        
        return None

    def _search_in_dynamoDB(
        self,
        date
    ):
        host = self.aws_url + '/search_holiday_db' + "?date=" + str(date)
        response = requests.get(host,headers=None)

        data = json.loads(response.content)
        for i in range(31):
            if(str(i) in data):
                print(data[str(i)][0]['holiday']['S'], data[str(i)][0]['date']['N'])
        return response.content
    
    def _upload_to_dynamoDB(
        self,
        datas
    ):
        host = self.aws_url + '/add_holiday_to_db'
        for single_data in datas :
            json_data = json.dumps(single_data, ensure_ascii=False)
            response = requests.post(host, json = json_data, headers=None)

        return response

    def update_dynamoDB(
        self,
        solYear,
        solMonth
    ):

        response = self._make_get_request(solYear,solMonth)
        parsed_response = self._parse_response(response)
        post_response = self._upload_to_dynamoDB(parsed_response)

        return post_response
