from pymongo import MongoClient
import json
import pickle

from NEAT.Analyst.AnalysisResult import AnalysisResult
from NEAT.GenomeStructures.StorageStructure.StorageGenome import StorageGenome


class DatabaseConnector(object):
    def __init__(self, database_name: str, client: MongoClient = MongoClient()):
        self._client = client
        self._database = self._client[database_name]

    def get_collection(self, collection_name: str):
        self._database[collection_name].find()
        return self._database[collection_name]

    def store_object_in_collection(
            self,
            collection_name: str,
            obj: object):
        jsoned_object = json.dumps(obj, cls=CustomJSONEncoder)
        self._database[collection_name].insert_one(jsoned_object)

    def find_object_in_collection(
            self,
            collection_name: str,
            object_id: int):
        obj = self._database[collection_name].find_one(object_id)
        return json.loads(obj, cls=CustomJSONDecoder)


class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, StorageGenome):
            return {'storage_genome_repr': obj.__dict__}
        elif isinstance(obj, AnalysisResult):
            return {'analysis_result_repr': pickle.dumps(obj).decode('latin1')}
        return json.JSONEncoder.default(self, obj)


class CustomJSONDecoder(json.JSONDecoder):
    def __init__(self):
        json.JSONDecoder.__init__(self, object_hook=self.hook)

    @staticmethod
    def hook(dct):
        if 'storage_genome_repr' in dct:
            s = StorageGenome()
            s.__dict__ = dct['storage_genome_repr']
            return s
        elif 'analysis_result_repr' in dct:
            return pickle.loads(dct['analysis_result_repr'].encode('latin1'))
        return dct
