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
    for part in ['part_1']:
        data = load_data(part)
        insert_data(data)
        # print(f'inserted {(index+1) * 1000 }')

    return 0





def insert_data(data: list, index='tweets'):
    bulk_string = ''
    number_of_doc_in_bulk = 0
    for doc in data:
        print(number_of_doc_in_bulk)
        doc_json = json.loads(doc['data'])
        if doc_json['location']['lat'] is None:
            doc_json['location'] = None
        
        doc_id = doc_json['id']
        # doc_id = re.match('^{"id": "[0-9]+', doc_string).__getitem__(0)[8:]
        doc_string = json.dumps(doc_json)
        action_string = f'{{\"index\":{{"_id": "{doc_id}" }}}}'
        bulk_string = bulk_string + action_string+ "\n" + doc_string + "\n"
        number_of_doc_in_bulk += 1
        if (number_of_doc_in_bulk % 1000) == 0:
            response = requests.post(f"http://192.168.0.101:9200/{index}/_bulk",
                                        data = bulk_string.encode("UTF-8"), 
                                        headers = {"Content-Type":"application/json; charset=utf-8"})
            response_json = json.loads(response.content.decode('utf-8'))
        
            if response_json['error']:
                raise Exception('problem')

            bulk_string = ''
            print('inserted {number_of_doc_in_bulk}')

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