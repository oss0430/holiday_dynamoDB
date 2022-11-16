import requests
import json 
from urllib.parse import urlencode
## Get Public Data
#url = 'http://apis.data.go.kr/B090041/openapi/service/SpcdeInfoService/getAnniversaryInfo'
#params ={'serviceKey' : data['key_decoding'], 'pageNo' : '1', 'numOfRows' : '10', 'solYear' : '2019', 'solMonth' : '02' }

#response = requests.get(url, params=params)
#print(type(response))
#print(response.text, type(response.text))
#response_data = response.json()
#print(response_data)
#print(response.content.body)


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
        parsed_list = []
        for dict in list_response:
            parsed_list.append({"date" : str(dict['locdate'])[2:],"sortdate" : str(dict['locdate'])[2:6],"holiday" : str(dict['dateName'])})
        
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
        print(response.text)
        data = json.loads(response.content)
        for i in range(31):
            if(str(i) in data):
                print(data[str(i)][0]['holiday']['S'], data[str(i)][0]['date']['N'])
        return response.content
        '''
        data = json.loads(response.content)
        print(json.dumps(data, ensure_ascii=False, indent=3))
        '''
    
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
        
        
my_data_updater = DataUpdater()
my_data_updater.load_public_api_with_json("public_data_api.json")
my_data_updater.load_aws_api_with_json("api_end_points.json")
print(json.dumps(json.loads(my_data_updater._make_get_request('2022', '12').content), ensure_ascii=False, indent=4))
print(my_data_updater._parse_response(my_data_updater._make_get_request('2019', '12')))
print("====================")
#my_data_updater.update_dynamoDB('2019', '12')
my_data_updater._search_in_dynamoDB(1912)
my_data_updater._search_in_dynamoDB(2012)