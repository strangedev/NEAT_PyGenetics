import unittest
from unittest.mock import MagicMock

from NEAT.GenomeStructures.StorageStructure.StorageGenome import StorageGenome
from NEAT.Repository.DatabaseConnector import DatabaseConnector


class DatabaseConnectorTest(unittest.TestCase):
    def setUp(self):
        client = MagicMock()
        client["testbase"] = MagicMock()
        self.collection = client["testbase"]

        self.database_connector = DatabaseConnector("testBase", client)

    def test_insertOne(self):
        self.collection.insert = True
        self.assertTrue(self.database_connector.insert_one("testbase", {}))

    def test_insertMany(self):
        self.collection.insert = True
        test_list = []
        for i in range(1, 10):
            test_list.append({})
        for i in self.database_connector.insert_many("testbase", test_list):
            self.assertTrue(i)
    
    def test_findOne(self):
        self.fail()

    def test_findOneById(self):
        self.fail()

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