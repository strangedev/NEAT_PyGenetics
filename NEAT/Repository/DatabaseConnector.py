from typing import Dict, Iterable, List, Tuple

from bson import ObjectId
from pymongo import MongoClient
import json
import pickle
from NEAT.Repository.Transformator import *


class DatabaseConnector(object):
    def __init__(self, database_name: str, client: MongoClient = MongoClient()):
        self._client = client
        self._database = self._client[database_name]

    def get_collection(self, collection_name: str):
        self._database[collection_name].find()
        return self._database[collection_name]

    def insert_one(
            self,
            collection_name: str,
            document: object
    ) -> int:
        """
        Inserts a single object into the given collection in the database.
        :param collection_name:
        :param document:
        :return:
        """
        if collection_name == "genomes":
            i = encode_StorageGenome(document)
            return self._database[collection_name].insert(i)
        else:
            return None

    def insert_many(
            self,
            collection_name: str,
            documents: Iterable[object]
    ) -> List[int]:
        """
        Inserts multiple objects into the given collection in the database.
        :param collection_name:
        :param documents:
        :return:
        """
        if collection_name == "genomes":
            result_ids = []
            for document in documents:
                i = encode_StorageGenome(document)
                result_ids.append(
                    self._database[collection_name].insert(i)
                )
            return result_ids
        else:
            return None

    def find_one(
            self,
            collection_name: str,
            filter: Dict
    ) -> object:
        """
        Finds a single document in the given collection. Same parameters as py-
        mongos default find_one, except for the collection_name.
        :param collection_name:
        :param filter:
        :return:
        """
        if collection_name == "genomes":
            o = self._database[collection_name].find_one(filter)
            return decode_StorageGenome(o)
        else:
            return None

    def find_one_by_id(
            self,
            collection_name: str,
            document_id
    ):
        """
        Finds a single document in the given collection based on its id.
        :param collection_name:
        :param document_id:
        :return:
        """
        if collection_name == "genomes":
            return decode_StorageGenome(self._database[collection_name].find_one({'_id': document_id}))
        else:
            return None

    def find_many(
            self,
            collection_name: str,
            filter: Dict
    ) -> Iterable[object]:
        """
        Finds all objects in the given collection that match a given query.
        Parameters the same as pymongos default find, except for the collection_
        name.
        :param collection_name:
        :param filter:
        :return:
        """
        if collection_name == "genomes":
            result = []
            found = self._database[collection_name].find(filter)
            for doc in found:
                result.append(decode_StorageGenome(doc))
            return result
        else:
            return None

    def update_one(
            self,
            collection_name: str,
            document_id: int,
            document: object
    ):
        """
        Updates a single document in the given collection in the database. Takes
        an id and an object and replaces the data at the given id with the ob-
        ject.
        :param document:
        :param document_id:
        :param collection_name:
        :return:
        """
        if collection_name == "genomes":
            doc = encode_StorageGenome(document)
            self._database[collection_name].update({'_id': document_id}, doc)

    def update_many(
            self,
            collection_name: str,
            documents: Iterable[Tuple[int, object]]
    ):
        """
        Updates multiple documents in the given collection in the database.
        Takes an Iterable of document_id, object tuples and replaces them one by
        one in the database.
        :param collection_name:
        :param documents:
        :return:
        """
        if collection_name == "genomes":
            for document_id, document in documents:
                doc = encode_StorageGenome(document)
                self._database[collection_name].update({'_id': document_id}, doc)

    def remove_one(
            self,
            collection_name: str,
            document_id
    ):
        """
        Removes one document by id from a given collection.
        :param collection_name:
        :param document_id:
        :return:
        """
        if collection_name == "genomes":
            self._database[collection_name].remove({'_id': document_id})

    def remove_many(
            self,
            collection_name: str,
            document_ids: Iterable[int]
    ):
        """
        Removes many documents by id from a given collection.
        :param collection_name:
        :param document_ids:
        :return:
        """
        if collection_name == "genomes":
            for document_id in document_ids:
                self._database[collection_name].remove({'_id': document_id})


class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, StorageGenome):
            return {'storage_genome_repr': obj.__dict__}
        elif isinstance(obj, AnalysisResult):
            return {'analysis_result_repr': pickle.dumps(obj).decode('latin1')}
        elif isinstance(obj, ObjectId):
            return str(obj)
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
        if '_id' in dct:
            dct['_id'] = ObjectId(dct['_id'])
        return dct
