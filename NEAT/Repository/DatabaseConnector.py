from typing import Dict, Iterable, List, Tuple

from bson import ObjectId
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
        if not hasattr(document, '_id') or document._id is None:
            document._id = ObjectId()
        obj_json = json.dumps(document, cls=CustomJSONEncoder)
        return self._database[collection_name].insert_one(obj_json)

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
        result_ids = []
        for document in documents:
            result_ids.append(
                self.insert_one(collection_name, document)
            )
        return result_ids

    def find_one(
            self,
            collection_name: str,
            *args, **kwargs
    ) -> object:
        """
        Finds a single document in the given collection. Same parameters as py-
        mongos default find_one, except for the collection_name.
        :param collection_name:
        :param args:
        :param kwargs:
        :return:
        """
        obj_json = self._database[collection_name].find_one(args, kwargs)
        self._database[collection_name].find_one()
        return json.loads(obj_json, cls=CustomJSONDecoder)

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
        return self.find_one(collection_name, {'_id': document_id})

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
        result = []
        for doc in self._database[collection_name].find(filter):
            result.append(json.loads(doc, cls=CustomJSONDecoder))

        return result

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
        obj_json = json.dumps(document, cls=CustomJSONEncoder)
        self._database[collection_name]\
            .replace_one({'_id': document_id}, obj_json)

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
        for document_id, document in documents:
            self.update_one(collection_name, document_id, document)

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
        self._database[collection_name].remove(document_id)

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
        for document_id in document_ids:
            self.remove_one(collection_name, document_id)


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
