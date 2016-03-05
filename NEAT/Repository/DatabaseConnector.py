from typing import Dict, Iterable, List, Tuple

from pymongo import MongoClient


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
            document: object
    ) -> int:
        """
        Inserts a single object into the given collection in the database.
        :param collection_name:
        :param document:
        :return:
        """
        try:
            return self._database[collection_name].insert(document)
        except Exception as e:
            print(e, 'insert_one, DatabaseConnector')

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
            try:
                i = self._database[collection_name].insert(document)
            except Exception as e:
                print(e, 'insert_many, DatabaseConnector')
            result_ids.append(i)
        return result_ids

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
        try:
            return self._database[collection_name].find_one(filter)
        except Exception as e:
            print(e, 'find_one, DatabaseConnector')

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
        try:
            return self._database[collection_name].find_one({'_id': document_id})
        except Exception as e:
            print(e, 'find_one_by_id, DatabaseConnector')

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
        try:
            return self._database[collection_name].find(filter)
        except Exception as e:
            print(e, 'find_many, DatabaseConnector')

    def update_one(
            self,
            collection_name: str,
            document_id,
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
        try:
            self._database[collection_name].update({'_id': document_id}, document)
        except Exception as e:
            print(e, 'update_one, DatabaseConnector')

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
            try:
                self._database[collection_name].update({'_id': document_id}, document)
            except Exception as e:
                print(e, 'update_many')

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
        try:
            self._database[collection_name].remove({'_id': document_id})
        except Exception as e:
            print(e, 'remove_one, DatabaseConnector')

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
                try:
                    self._database[collection_name].remove({'_id': document_id})
                except Exception as e:
                    print(e, 'remove_many, DatabaseConnector')
