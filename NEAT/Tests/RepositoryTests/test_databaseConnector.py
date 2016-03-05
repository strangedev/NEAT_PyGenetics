import unittest
from unittest.mock import MagicMock
from json import loads, dumps

from NEAT.GenomeStructures.StorageStructure.StorageGenome import StorageGenome
from NEAT.Repository.DatabaseConnector import DatabaseConnector
from NEAT.Repository.Transformator import CustomJSONDecoder
from NEAT.Repository.Transformator import CustomJSONEncoder


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

    def test_insertOne(self):
        s = StorageGenome()
        self.database_connector.insert_one("testcollection", s)
        res = loads(self.collection.insert_one.call_args_list[0][0][0],
                    cls=CustomJSONDecoder)

        self.assertEqual(s, res)

    def test_insertMany(self):
        documents = []
        for i in range(10):
            s = StorageGenome()
            s.cluster = i
            documents.append(s)
        self.database_connector.insert_many("testcollection", documents)

        res = []
        for call in self.collection.insert_one.call_args_list:
            res.append(loads(call[0][0], cls=CustomJSONDecoder))

        self.assertListEqual(documents, res)

    def test_findOne(self):
        s = StorageGenome()
        s.cluster = 5
        s_json = dumps(s, cls=CustomJSONEncoder)
        self.collection.find_one = MagicMock(return_value=s_json)
        res = self.database_connector.find_one("testcollection", {'cluster': 5})
        self.assertEqual(s, res)

    def test_findOneById(self):
        s = StorageGenome()
        s_json = dumps(s, cls=CustomJSONEncoder)
        self.collection.find_one = MagicMock(return_value=s_json)
        res = self.database_connector.find_one_by_id("testcollection", 0)
        self.assertEqual(s, res)

    def test_find(self):
        self.fail()

    def test_updateOne(self):
        self.fail()

    def test_updateMany(self):
        self.fail()

    def test_removeOne(self):
        self.fail()

    def test_removeMany(self):
        self.fail()