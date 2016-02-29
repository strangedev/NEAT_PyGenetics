import unittest
from unittest.mock import MagicMock
from json import loads, dumps

from NEAT.GenomeStructures.StorageStructure.StorageGenome import StorageGenome
from NEAT.Repository.DatabaseConnector import DatabaseConnector
from NEAT.Repository.DatabaseConnector import CustomJSONDecoder
from NEAT.Repository.DatabaseConnector import CustomJSONEncoder


class DatabaseConnectorTest(unittest.TestCase):
    def setUp(self):
        self.collection = MagicMock()
        self.db = MagicMock()
        self.db.__getitem__ = MagicMock(return_value=self.collection)
        self.client = MagicMock()
        self.client.__getitem__ = MagicMock(return_value=self.db)
        self.client["testdb"] = self.db
        self.client["testdb"]["testcollection"] = self.collection

        self.database_connector = DatabaseConnector("testdb", self.client)

    def test_storeObject(self):
        s = StorageGenome()
        self.database_connector.store_object_in_collection("testcollection", s)
        res = loads(self.collection.insert_one.call_args_list[0][0][0],
                    cls=CustomJSONDecoder)

        self.assertEqual(s, res)

    def test_retrieveObject(self):
        s = StorageGenome()
        s_json = dumps(s, cls=CustomJSONEncoder)
        self.collection.find_one = MagicMock(return_value=s_json)
        res = self.database_connector.find_object_in_collection("testcollection", 0)
        self.assertEqual(s, res)
