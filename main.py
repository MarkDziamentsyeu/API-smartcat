import requests
import json
from requests.auth import HTTPBasicAuth


def open_config():
    """Open and parse the configuration file config_dict.txt"""

    with open("config_dict.txt","r") as f:
        config = f.read() 

    params = {}


    pairs = config.split("\n")


    for pair in pairs:
        key_value = pair.split(":")
        key = key_value[0]
        value = key_value[-1]

        params[key] = value

    return params


def put_glossary(project_id):
    """The function passes a collection of glossaries to the created project"""

    account_id = 'ACCOUNT_ID'   # in your personal account
    key = 'KEY'                 # create in your personal account                
    base_url = f'https://smartcat.ai/api/integration/v1/project/{project_id}/glossaries'
    auth = HTTPBasicAuth(account_id, key)

    params = open_config()
    glossary_id = params['glossary']
    data = f'[{glossary_id}]'


    response = requests.put(url=base_url, data=data, auth=auth) 


    if response.status_code == 204:
        print('Glossary added successfully')

    else:
        print('An error occurred in adding the glossary. Response:', response.text)




def add_tm(project_id, new_tm_id): 
    """The function that adds TM to the project, one TM is new, and we take the second one from the configuration file, if it is specified"""

    account_id = "ACCOUNT_ID"
    key = 'KEY'
    base_url = f'https://smartcat.ai/api/integration/v1/project/{project_id}/translationmemories'
    auth = HTTPBasicAuth(account_id, key)

     
    params = open_config()

    if 'null' in params['id_TM']:           #if do not add an existing TM, then we create a new empty TM in create_tm()
        new_tm_id = f'"{new_tm_id}"'
        data = "[\n {\n   \
                \"id\": "f'{new_tm_id}'",\n  \
                \"matchThreshold\": 50,\n \
                \"isWritable\": true\n }\n]"
        
        
    else:                                  #Adding an existing TM and a new one created in create_tm()
        new_tm_id = f'"{new_tm_id}"'  
        id_TM = params['id_TM']
        data = "[\n {\n   \
                \"id\": "f'{new_tm_id}'",\n  \
                \"matchThreshold\": 75,\n \
                \"isWritable\": true\n },\n \
                {\n   \
                \"id\": "f'{id_TM}'",\n  \
                \"matchThreshold\": 75,\n \
                \"isWritable\": false\n },\n]"


    headers = {
    "Content-Type": "application/json-patch+json",
    "accept": "*/*"
    }

    response = requests.post(url=base_url,headers=headers, data=data, auth=auth) 

    
    if response.status_code == 200:
        print('TM added successfully.')

    else:
        print('An error occurred in adding TM. Response:', response.text)



def create_tm():
    "Creating a new TM specifically for the project, which we will then pass to the add_tm()"

    account_id = "ACCOUNT_ID"
    key = 'KEY'
    base_url = 'https://smartcat.ai/api/integration/v1/translationmemory'
    auth = HTTPBasicAuth(account_id, key)

    params = open_config()


    name = params['name']
    sourceLanguage =  params['sourceLanguage']
    targetLanguages =  params['targetLanguages']
    description  =  params['description']

    data =  "{\n  \
            \"name\": "f'{name}'",\n  \
            \"sourceLanguage\": "f'{sourceLanguage}'",\n  \
            \"targetLanguages\": [\n    "f'{targetLanguages}'",\n   ],\n  \
            \"description\": "f'{description}'",\n}\n".encode('utf-8')
    
 
      
    response = requests.post(url=base_url, data=data, auth=auth)
    project_data = response.json()   
    new_tm_id = project_data

    if response.status_code == 201:
        print('TM was created successfully.')

    else:
        print('An error occurred in creating the TM. Response:', response.text)

    return new_tm_id



def add_file(project_id):
    """Add a file to the project if you need to add several documents at once"""
    
    account_id = 'ACCOUNT_ID'
    key = 'KEY'
    auth = HTTPBasicAuth(account_id, key)

    params = open_config()

    file_path = params["file_path"].split(",")

    for i in range(len(file_path)):
        file_path[i] = file_path[i].strip()
   

    targetLanguages = params['targetLanguages']
    sourceLanguage = params['sourceLanguage']
    deadline = params['deadline']
 

    data = {
        "value": "[\n  {\n    \
            \"externalId\": null,\n  \
            \"deadline\": "f'{deadline}'",\n  \
            \"bilingualFileImportSetings\": {\n      \
            \"targetSubstitutionMode\": \"all\",\n      \
            \"lockMode\": \"none\",\n      \
            \"confirmMode\": \"none\"\n    },\n    \
            \"sourceLanguage\": "f'{sourceLanguage}'",\n  \
            \"targetLanguages\": [\n    "f'{targetLanguages}'",\n  ],\n  \
            \"enablePlaceholders\": true,\n    \
            \"enableOcr\": true\n  }\n]"
            }

    j = 0
    for file in file_path:  
        j+=1
        print(file)
        with open(file, 'rb') as f:
            file_content = f.read()

        files = {
        'file': (file, file_content, 'multipart/form-data')
    }

        url = f'https://smartcat.ai/api/integration/v1/project/document?projectId={project_id}'
        response = requests.post(url, auth=auth, data=data, files=files)


        if response.status_code == 200:
            print('The document was added successfully.')

        else:
            print('An error occurred in adding the document. Response:', response.text)


        file_path = params["file_path"].split(",")
        id_lingvist_list = params['id_lingvist'].split(",")
        id_redactor_list = params['id_redactor'].split(",")
        
        if len(file_path) == len(id_lingvist_list):
            document_data = response.json()
            document_id = document_data[0]['id']
        
            post_lingvist(document_id, j) #assign a linguist for the added document
                

        else:
            print("Not all documents have linguists assigned to them")


        if len(file_path) == len(id_redactor_list):
            document_data = response.json()
            document_id = document_data[0]['id']
        
            post_redactor(document_id, j)  #assign an editor for the added document
                

        else:
            print("Not all documents have editors assigned to them")

        

        

def add_file_one(project_id):
    """Add a file to the project if you need to add only one document"""

    account_id = 'ACCOUNT_ID'
    key = 'KEY'
    auth = HTTPBasicAuth(account_id, key)

    params = open_config()

    file_path = params['file_path'].strip()

 
    with open(file_path, 'rb') as f:
        file_content = f.read()

   
    files = {
        'file': (file_path, file_content, 'multipart/form-data')
    }

    
    targetLanguages = params['targetLanguages']
    sourceLanguage = params['sourceLanguage']
    deadline = params['deadline']

    data = {
        "value": "[\n  {\n    \
            \"externalId\": null,\n  \
            \"deadline\": "f'{deadline}'",\n  \
            \"bilingualFileImportSetings\": {\n      \
            \"targetSubstitutionMode\": \"all\",\n      \
            \"lockMode\": \"none\",\n      \
            \"confirmMode\": \"none\"\n    },\n    \
            \"sourceLanguage\": "f'{sourceLanguage}'",\n  \
            \"targetLanguages\": [\n    "f'{targetLanguages}'",\n  ],\n  \
            \"enablePlaceholders\": true,\n    \
            \"enableOcr\": true\n  }\n]"
            }


    url = f'https://smartcat.ai/api/integration/v1/project/document?projectId={project_id}'
    response = requests.post(url, auth=auth, data=data, files=files)


    if response.status_code == 200:
        print('The document was added successfully.')

    else:
        print('An error occurred in adding the document. Response:', response.text)

    document_data = response.json()

    targetLanguages_list = params['targetLanguages'].split(",")
    for j in range(1,len(targetLanguages_list)+1):
        document_id = document_data[j-1]['id']
        if 'null' not in params["id_lingvist"]:
            post_lingvist(document_id, j)

        if 'null' not in params["id_redactor"]:
            post_redactor(document_id, j)


def post_lingvist(document_id, j):
    """The function assigns a linguist to a specific stage of the project"""

    account_id = 'ACCOUNT_ID'
    key = 'KEY'
    base_url = f'https://smartcat.ai/api/integration/v1/document/assign?documentId={document_id}&stageNumber=1'
    auth = HTTPBasicAuth(account_id, key)

    params =  open_config()

    id_lingvist_list = params['id_lingvist'].split(",")
   
    for i in range(len(id_lingvist_list)):
        id_lingvist_list[i] = id_lingvist_list[i].strip()

    id_lingvist = id_lingvist_list[j-1]

    if id_lingvist != "null":
        data_2 = "{\n  \
        \"executives\": [\n  \
        {\n  \
        \"id\": "f'{id_lingvist}'",\n }\n  \
        ],\n  \
        \"minWordsCountForExecutive\": 0, \n  \
        \"assignmentMode\": \"InviteOnly\" \n  \
        }"
        
        
        headers = {
        "Content-Type": "application/json-patch+json",
        "accept": "*/*"
        }

        response = requests.post(url=base_url, headers=headers, data=data_2, auth=auth) 

        if response.status_code == 204:
            print('Linguist added successfully.')

        else:
            print('An error occurred in adding a linguist. Response:', response.text)

    
    else:
        print("There is no linguist assigned to this document")


def post_redactor(document_id, j):
    """Функция назначает лингвиста на определённый этап проекта"""

    account_id = 'ACCOUNT_ID'
    key = 'KEY'
    base_url = f'https://smartcat.ai/api/integration/v1/document/assign?documentId={document_id}&stageNumber=2'
    auth = HTTPBasicAuth(account_id, key)

    
    params =  open_config()


    id_redactor_list = params['id_redactor'].split(",")
   

    for i in range(len(id_redactor_list)):
        id_redactor_list[i] = id_redactor_list[i].strip()

    id_redactor = id_redactor_list[j-1]

    if id_redactor != "null":
        data_2 = "{\n  \
                \"executives\": [\n  \
                {\n  \
                \"id\": "f'{id_redactor}'",\n }\n  \
                ],\n  \
                \"minWordsCountForExecutive\": 0, \n  \
                \"assignmentMode\": \"InviteOnly\" \n  \
                }"
        

        headers = {
        "Content-Type": "application/json-patch+json",
        "accept": "*/*"
        }


        response = requests.post(url=base_url, headers=headers, data=data_2, auth=auth) 


        if response.status_code == 204:
            print('The editor was added successfully.')

        else:
            print('An error occurred while adding the editor. Response:', response.text)

    
    else:
        print("There is no editor assigned to this document")


def create():
    """The function that creates the project"""

    account_id = 'ACCOUNT_ID'
    key = 'KEY'
    base_url = 'https://smartcat.ai/api/integration/v1/project/create'
    auth = HTTPBasicAuth(account_id, key)


    params = open_config()


    name = params["name"]
    sourceLanguage = params["sourceLanguage"]
    targetLanguages = params["targetLanguages"]
    deadline = params["deadline"]
    description = params["description"]
    workflowStages = params["workflowStages"]
    externalTag = params["externalTag"]
    clientId = params["clientId"]
    creatorUserId = params["creatorUserId"]

    
    
    data = {
        "value": "{\n  \
            \"name\": "f'{name}'",\n  \
            \"sourceLanguage\": "f'{sourceLanguage}'",\n  \
            \"targetLanguages\": [\n    "f'{targetLanguages}'",\n  ],\n  \
            \"deadline\": "f'{deadline}'",\n \
            \"description\": "f'{description}'",\n \
            \"creatorUserId\": "f'{creatorUserId}'",\n \
            \"assignToVendor\": false,\n  \
            \"useMT\": false,\n  \
            \"pretranslate\": true,\n  \
            \"useTranslationMemory\": true,\n  \
            \"autoPropagateRepetitions\": true,\n  \
            \"workflowStages\": null,\n  \
            \"isForTesting\": false,\n  \
            \"externalTag\": "f'{externalTag}'",\n \
            \"clientId\": "f'{clientId}'",\n \
            \"enableProjectTasks\":true,\n}\n".encode('utf-8')
            }

    
    response = requests.post(url=base_url, data=data, auth=auth)

    
    if response.status_code == 200:
        print('The project was added successfully.')

    else:
        print('An error occurred while adding the project. Response:', response.text)

    
    project_data = response.json()   #get the parameters of the created project
    project_id = project_data['id']


    if 'null' not in params['file_path']:
        file_path = params["file_path"].split(",")
        

        if len(file_path) == 1: #if 1 document is specified in the configuration file, we call the function
            add_file_one(project_id)

        else:                  #if several documents are specified in the configuration file, we call the function
            add_file(project_id)

            
    new_tm_id = create_tm()         #creating a new TM for a new project
    add_tm(project_id,new_tm_id)    #adding a TM to a new project
    

    if 'null' not in params['glossary']:   #if a glossary is specified in the configuration file, we call the function to add a glossary
        put_glossary(project_id)




if __name__ == '__main__':
    create()






    








