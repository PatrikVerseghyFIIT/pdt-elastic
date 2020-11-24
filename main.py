import json
import requests
import re
import numpy as np

from elasticsearch import Elasticsearch
from elasticsearch_dsl import Index
from elasticsearch_dsl import connections

es = Elasticsearch(hosts='192.168.0.101:9200',)

def create_elastic_index(index_name: str, number_of_shards: int = 3, number_of_replications: int = 2):
    with open('mapping.json') as f:
        elastic_mapping = json.load(f)

    elastic_mapping['settings']['index'] = {
                                            "number_of_shards": number_of_shards,  
                                            "number_of_replicas": number_of_replications 
                                            }

    return es.indices.create(index='tweets',body=elastic_mapping)
    

def load_data(file_name: str):
    with open(f'data/{file_name}.json') as f:
        data = json.load(f)

    return data

def main():
    #print(create_elastic_index('tweets'))
    # print(es.indices.exists('tweets'))
    for part in ['part_2','part_3', 'part_4', 'part_5', 'part_6', 'part_7']
        data = load_data(part)
        
        iter_data = np.array_split(data, 1000)
        for index, list_of_data in enumerate(iter_data):
            inser_data(list_of_data)
            print(f'inserted {(index+1) * 1000 }')

    return 0





def inser_data(data: list, index='tweets'):
    bulk_string = ''
    for doc in data:
        doc_string = doc['data']
        doc_id = re.match('^{"id": "[0-9]+', doc_string).__getitem__(0)[8:]
        action_string = f'{{\"index\":{{"_id": "{doc_id}" }}}}'
        bulk_string = bulk_string + action_string+"\n"+ doc_string + "\n"
    
    response = requests.post(f"http://192.168.0.101:9200/{index}/_bulk",
                                data = bulk_string.encode("UTF-8"), 
                                headers = {"Content-Type":"application/json; charset=utf-8"})
    print(response.status_code)

if __name__ == "__main__":
    # execute only if run as a script
    main()



# def importData(index='tweets',mongoDB):
#     batchSize = 10000
#     bulkString = ""
#     for index,doc in enumerate(data):
#         ind = "{\"index\":{}}"
#         stringData=json.dumps(doc)
#         bulkString = bulkString + ind+"\n"+ stringData + "\n"
#         if index%batchSize == 0 and index!=0:
#             response = requests.post(f"http://localhost:9200/{index}/_bulk", data = bulkString.encode("UTF-8"), headers = {"Content-Type":"application/json; charset=utf-8"})
#             bulkString = ""
#             print("odoslanych ",index,response.text)
#     response = requests.post(f"http://localhost:9200/{index}/_bulk", data = bulkString.encode("UTF-8"), headers = {"Content-Type":"application/json; charset=utf-8"})
#     bulkString = ""
#     print("odoslanych ",index,response)