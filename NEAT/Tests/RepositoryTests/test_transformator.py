import copy
import unittest
from unittest import TestCase

from NEAT.Analyst.AnalysisResult import AnalysisResult
from NEAT.GenomeStructures.StorageStructure.StorageGenome import StorageGenome
from NEAT.Repository.Transformator import Transformator


class TestTransformator(TestCase):

    def test_encode_AnalysisResult(self):
        analysis_result = AnalysisResult()
        dictionary = copy.deepcopy(analysis_result.__dict__)
        dictionary.__setitem__('_type', 'AnalysisResult')
        self.assertDictEqual(dictionary, Transformator.encode_AnalysisResult(analysis_result))

    def test_encode_StorageGenome(self):
        storage_genome = StorageGenome()
        storage_dict = copy.deepcopy(storage_genome.__dict__)
        analysis_dict = Transformator.encode_AnalysisResult(storage_dict.__getitem__('analysis_result'))
        storage_dict.__setitem__('analysis_result', analysis_dict)
        storage_dict.__setitem__('_type', 'StorageGenome')
        self.assertDictEqual(storage_dict, Transformator.encode_StorageGenome(storage_genome))

    def test_decode_AnalysisResult(self):
        analysis_result = AnalysisResult()
        dict = analysis_result.__dict__
        dict.__setitem__('_type', 'AnalysisResult')
        self.assertTrue(analysis_result.__eq__(Transformator.decode_AnalysisResult(dict)))

    def test_decode_StorageGenome(self):
        storage_genome = StorageGenome()
        analysis_stor = storage_genome.__dict__.__getitem__('analysis_result')
        analysis_dict = Transformator.encode_AnalysisResult(analysis_stor)
        stor = copy.deepcopy(storage_genome.__dict__)
        stor.__setitem__('analysis_result', analysis_dict)
        stor.__setitem__('_type', 'StorageGenome')
        self.assertTrue(storage_genome.__eq__(Transformator.decode_StorageGenome(stor)))

    @unittest.expectedFailure
    def test_encode_AnalysisResultExpectedKeyError(self):
        e = {}
        self.assertEqual(None, Transformator.encode_AnalysisResult(e))

    @unittest.expectedFailure
    def test_decodeAnalysisResultExpectedKeyError(self):
        self.assertEqual(None, Transformator.decode_AnalysisResult({}))

    @unittest.expectedFailure
    def test_encode_StorageGenome(self):
        self.assertEqual(None, Transformator.encode_StorageGenome({}))
