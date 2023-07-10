import requests
import json
from requests.auth import HTTPBasicAuth


def get_all_glossarys():
    """The function collects all created glossaries and writes them to the glossary.json file"""

    
    account_id = 'ACCOUNT_ID'
    key = 'KEY'
    base_url = 'https://smartcat.ai/api/integration/v1/glossaries'
    auth = HTTPBasicAuth(account_id, key)
    
    data = []

    response = requests.get(url=base_url, auth=auth) 


    data.append(response.json())

    with open("glosary.json", 'w') as file:
         json.dump(data, file, indent=3, ensure_ascii=False)




if __name__ == '__main__':
    get_all_glossarys()




