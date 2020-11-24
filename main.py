import json
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
    
def main():
    #print(create_elastic_index('tweets'))
    # print(es.indices.exists('tweets'))

    return 0

def importData(index='tweets',mongoDB):
    batchSize = 10000
    bulkString = ""
    for index,doc in enumerate(data):
        ind = "{\"index\":{}}"
        stringData=json.dumps(doc)
        bulkString = bulkString + ind+"\n"+ stringData + "\n"
        if index%batchSize == 0 and index!=0:
            response = requests.post(f"http://localhost:9200/{index}/_bulk", data = bulkString.encode("UTF-8"), headers = {"Content-Type":"application/json; charset=utf-8"})
            bulkString = ""
            print("odoslanych ",index,response.text)
    response = requests.post(f"http://localhost:9200/{index}/_bulk", data = bulkString.encode("UTF-8"), headers = {"Content-Type":"application/json; charset=utf-8"})
    bulkString = ""
    print("odoslanych ",index,response)

def inser_data(data: list):
    bulk_string = ''
    for index,doc in enumerate(data):
        action_string = f'{{\"index\":{{"_id":{doc["id"]} }}}}'
        document_string = json.dumps(doc)
        bulk_string = bulk_string + action_string+"\n"+ document_string + "\n"
    
    response = requests.post(f"http://localhost:9200/{index}/_bulk",
                                data = bulk_string, 
                                headers = {"Content-Type":"application/json"})

if __name__ == "__main__":
    # execute only if run as a script
    main()
