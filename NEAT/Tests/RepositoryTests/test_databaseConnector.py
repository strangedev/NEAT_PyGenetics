import unittest
from unittest.mock import MagicMock

from NEAT.GenomeStructures.StorageStructure.StorageGenome import StorageGenome
from NEAT.Repository.DatabaseConnector import DatabaseConnector


class DatabaseConnectorTest(unittest.TestCase):
    def setUp(self):
        client = MagicMock()
        client['testbase'] = MagicMock()
        self.db = client['testbase']
        self.collection = self.db['testbase']

        self.database_connector = DatabaseConnector("testBase", client)

    def test_insertOne(self):
        self.collection.insert = (lambda x: x)
        self.assertDictEqual({}, self.database_connector.insert_one('testbase', {}))

    def test_insertMany(self):
        self.collection.insert = (lambda x: x)
        test_list = []
        for i in range(1, 10):
            test_list.append({})
        self.assertListEqual(test_list, self.database_connector.insert_many("testbase", test_list))

    def test_findOne(self):
        self.collection.find_one = (lambda x: x)
        self.assertDictEqual({'x': 'y'}, self.database_connector.find_one('testbase', {'x': 'y'}))

    def test_findOneById(self):
        self.collection.find_one = (lambda x: x)
        self.assertDictEqual({'_id': '123'}, self.database_connector.find_one_by_id('testbase', '123'))

    def test_findMany(self):
        self.collection.find = (lambda x: x)
        self.assertDictEqual({'a': 'b', 'c': 'd'}, self.database_connector.find_many('testbase', {'a': 'b', 'c': 'd'}))

    def test_updateOne(self):
        self.collection.update = (lambda x, y: [x, y])
        self.database_connector.update_one('testbase', '22', {'test': 'test'})
        pass

    @unittest.expectedFailure
    def test_updateMany(self):
        self.collection.update = (lambda x, y: [x, y])
        self.fail(self.database_connector.update_many('testbase', [{'doc': 'doc'}]))
        self.database_connector.update_many('testbase', [(1, {'doc': 'doc'})])

    def test_removeOne(self):
        self.fail()

    def test_removeMany(self):
        self.fail()