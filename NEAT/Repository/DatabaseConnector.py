from typing import Dict, Iterable, List, Tuple, TypeVar

from bson import ObjectId
from pymongo import MongoClient

AnyId = TypeVar('AnyId', ObjectId, int, str)


class DatabaseConnector(object):
    def __init__(self, database_name: str, client: MongoClient = MongoClient()):
        self._client = client
        self._database = self._client[database_name]

    def get_collection(self, collection_name: str):
        # self._database[collection_name].find() # don't see why we need this
        return self._database[collection_name]

    def insert_one(
            self,
            collection_name: str,
            document: dict
    ) -> ObjectId:
        """
        Inserts a single object into the given collection in the database.
        :param collection_name:
        :param document:
        :return:
        """
        try:
            return self._database[collection_name].insert(document)
        except Exception as e:
            raise Exception(" insert_one, DatabaseConnector") from e

    def insert_many(
            self,
            collection_name: str,
            documents: Iterable[object]
    ) -> List[ObjectId]:
        """
        Inserts multiple objects into the given collection in the database.
        :param collection_name:
        :param documents:
        :return:
        """
        result_ids = []
        for document in documents:
            try:
                i = self._database[collection_name].insert(document)
                result_ids.append(i)
            except Exception as e:
                raise Exception(" insert_many, DatabaseConnector") from e
        return result_ids

    def find_one(
            self,
            collection_name: str,
            filter: Dict
    ) -> dict:
        """
        Finds a single document in the given collection. Same parameters as py-
        mongos default find_one, except for the collection_name.
        :param collection_name:
        :param filter:
        :return:
        """
        try:
            return self._database[collection_name].find_one(filter)
        except Exception as e:
            raise Exception(" find_one, DatabaseConnector") from e

    def find_one_by_id(
            self,
            collection_name: str,
            document_id: AnyId
    ) -> dict:
        """
        Finds a single document in the given collection based on its id.
        :param collection_name:
        :param document_id:
        :return:
        """
        try:
            return self._database[collection_name].find_one({'_id': document_id})
        except Exception as e:
            raise Exception(" find_one_by_id, DatabaseConnector") from e

    def find_many(
            self,
            collection_name: str,
            filter: Dict
    ) -> Iterable[dict]:
        """
        Finds all objects in the given collection that match a given query.
        Parameters the same as pymongos default find, except for the collection_
        name.
        :param collection_name:
        :param filter:
        :return:
        """
        try:
            return self._database[collection_name].find(filter)
        except Exception as e:
            raise Exception(" find_many, DatabaseConnector") from e

    def update_one(
            self,
            collection_name: str,
            document_id: AnyId,
            document: object
    ) -> dict:
        """
        Updates a single document in the given collection in the database. Takes
        an id and an object and replaces the data at the given id with the ob-
        ject.
        :param document:
        :param document_id:
        :param collection_name:
        :return: information about update process (from mongoDB)
        """
        try:
            return self._database[collection_name].update({'_id': document_id}, document)
        except Exception as e:
            raise Exception(" update_one, DatabaseConnector") from e

    def update_many(
            self,
            collection_name: str,
            documents: Iterable[Tuple[AnyId, object]]
    ) -> List[dict]:
        """
        Updates multiple documents in the given collection in the database.
        Takes an Iterable of document_id, object tuples and replaces them one by
        one in the database.
        :param collection_name:
        :param documents:
        :return: information about update process (from mongoDB)
        """
        result = []
        for document_id, document in documents:
            try:
                result.append(self._database[collection_name].update({'_id': document_id}, document))
            except Exception as e:
                raise Exception(" update_many, DatabaseConnector") from e
        return result

    def remove_one(
            self,
            collection_name: str,
            document_id: AnyId
    ):
        """
        Removes one document by id from a given collection.
        :param collection_name:
        :param document_id:
        :return:
        """
        try:
            return self._database[collection_name].remove({'_id': document_id})
        except Exception as e:
            raise Exception(" remove_one, DatabaseConnector") from e

    def remove_many(
            self,
            collection_name: str,
            document_ids: Iterable[AnyId]
    ):
        """
        Removes many documents by id from a given collection.
        :param collection_name:
        :param document_ids:
        :return:
        """
        result = []
        for document_id in document_ids:
            try:
                result.append(self._database[collection_name].remove({'_id': document_id}))
            except Exception as e:
                raise Exception(" remove_many, DatabaseConnector") from e
        return result
