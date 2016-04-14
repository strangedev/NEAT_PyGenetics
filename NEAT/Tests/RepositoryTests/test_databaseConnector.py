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
        self.database_connector = DatabaseConnector("testbase", client)

    def test_getCollection(self):
        self.assertTrue(self.collection.__eq__(\
                            self.database_connector.get_collection('testbase')))

    def test_insertOne(self):
        self.database_connector.insert_one('testbase', "blubb")
        self.assertListEqual(["blubb"], self.database_connector.query["testbase"])
        self.database_connector.insert_one('testbase', "test")
        self.assertListEqual(["blubb", "test"], self.database_connector.query["testbase"])

    def test_insertMany(self):
        self.database_connector.insert_many('testbase', ["blubb", 2, 3])
        self.assertListEqual(["blubb", 2, 3], self.database_connector.query["testbase"])
        self.database_connector.insert_many('testbase', ["test", 4, 5])
        self.assertListEqual(["blubb", 2, 3, "test", 4, 5], self.database_connector.query["testbase"])

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
        self.collection.update = (lambda x, y: True)
        self.assertTrue(
            self.database_connector.update_one('testbase', '22', {'test': 'test'}))

    @unittest.expectedFailure
    def test_updateManyFail(self):
        self.collection.update = (lambda x, y: [x, y])
        self.database_connector.update_many('testbase', [(1, {'doc': 'doc'})])
        self.fail(self.database_connector.update_many('testbase', [{'doc': 'doc'}]))

    def test_updateMany(self):
        self.collection.update = (lambda x, y: True)
        for i in self.database_connector.update_many(
                'testbase',
                [(1, {'doc': 'doc'}), (2, {'doc': 'doc'}), (1, {'doc': 'doc'}), (1, {'doc': 'doc'})]
        ):
            self.assertTrue(i)

    def test_removeOne(self):
        self.collection.remove = (lambda x: True)
        self.assertTrue(
            self.database_connector.remove_one('testbase', {'a': 2})
        )

    def test_removeMany(self):
        self.collection.remove = (lambda x: True)
        for i in self.database_connector.remove_many('testbase', [12, 2, 3]):
                self.assertTrue(i)

    def test_clearCollection(self):
        self.db.drop_collection = MagicMock()
        self.database_connector.clear_collection("testbase")
        self.db.drop_collection.assert_called_once_with("testbase")

    def test_insertQuery(self):
        self.database_connector._database["testbase"].insert = MagicMock(return_value=True)
        self.database_connector.query = {"testbase": [1,2,3,4]}
        self.assertListEqual([True, True, True, True], self.database_connector.insert_query("testbase"))
        self.database_connector._database["testbase"].insert.assert_any_call(1)
        self.database_connector._database["testbase"].insert.assert_any_call(2)
        self.database_connector._database["testbase"].insert.assert_any_call(3)
        self.database_connector._database["testbase"].insert.assert_any_call(4)