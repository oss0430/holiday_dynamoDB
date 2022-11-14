import requests
import json as jsonLoader
"""
    Search if DynamoDB has information for certain date (holiday)
    If the information do not match with public data, update it
"""


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
        key,
        url,
        table
    )-> None:
        self.key = key
        self.url = url
        self.table = table
    
    def _make_get_request(
        self,
        pageNo,
        numOfRows,
        solYear,
        solMonth
    )-> requests.models.Response :

        params ={'serviceKey' : self.key, 'pageNo' : str(pageNo), 'numOfRows' : str(numOfRows), 'solYear' : str(solYear), 'solMonth' : str(solMonth) }
        response = requests.get(self.url, params=params)
        return response

    def _parse_response(
        self,
        response
    ) -> dict:

        parsed = {}
        return parsed

    def load_public_api_with_json(
        self,
        file_path
    )-> None:
    
        with open(file_path, 'r') as file:
            data = jsonLoader.load(file)
            self.key = data['key_decoding']
            self.url = data['url']    


    def _search_in_dynamoDB(
        self,
        solYear,
        solMonth
    ):  
        ## Search if DynamoDB has the information
        return

    def _is_in_dynamoDB(
        self
    ) -> bool:
        
        
        return
    
    def _upload_to_dynamoDB(
        self,
        data
    ):
        return


    def update_dynamoDB(
        self,
        pageNo,
        numOfRows,
        solYear,
        solMonth
    ):
        if self._is_in_dynamoDB(solYear,solMonth) :
            return

        else :
            response = self._make_get_request(pageNo,numOfRows,solYear,solMonth)
            parsed_response = self._parse_response(response)
            self._upload_to_dynamoDB(parsed_response)

            return
