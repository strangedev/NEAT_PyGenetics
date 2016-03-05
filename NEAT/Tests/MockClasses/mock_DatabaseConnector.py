from typing import List, Iterable, Tuple, Dict

class mock_DatabaseConnector(object):

    def __init__(self):

        self._database = dict({})
        self._m_next_id = 0

    def get_collection(self, collection_name: str):
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
        self.create_collection_if_not_exists(collection_name)

        assigned_id = self.next_id
        document._id = assigned_id

        self._database[collection_name][assigned_id] = document

        return assigned_id

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
        self.create_collection_if_not_exists(collection_name)

        assigned_ids = []

        for document in documents:

            assigned_ids.append(
                self.insert_one(collection_name, document)
            )

        return assigned_ids

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
        if collection_name in self._database.keys():

            for doc_id, document in self._database[collection_name].items():

                for key, value in filter.items():

                    if key in document.keys():

                        if document[key] == value:
                            return document
                        else:
                            continue

                    else:
                        continue

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
        if collection_name in self._database.keys():

            for document in self._database[collection_name]:

                if document._id == document_id:
                    return document

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
        results = []

        if collection_name in self._database.keys():

            for document in self._database[collection_name]:

                for key, value in filter.items():

                    if key in document.keys():

                        if document[key] == value:
                            results.append(document)
                        else:
                            continue

                    else:
                        continue

        return results

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
        if collection_name in self._database.keys():

            for stored_document in self._database[collection_name]:

                if stored_document._id == document_id:

                     stored_document = document

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
        for doc_id, document in documents:
            self.update_one(collection_name, doc_id, document)

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
        pass

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

    def create_collection_if_not_exists(self, collection_name):
        if not collection_name in self._database.keys():
            self._database[collection_name] = dict({})

    @property
    def next_id(self):
        next_id = self._m_next_id
        self._m_next_id += 1
        return  next_id