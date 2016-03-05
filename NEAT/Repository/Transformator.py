import json
import pickle

from bson import ObjectId

from NEAT.Analyst.AnalysisResult import AnalysisResult
from NEAT.GenomeStructures.StorageStructure.StorageGenome import StorageGenome

def encode_AnalysisResult(analysis_result: AnalysisResult) -> dict:
    """
    encodes AnalysisResult in an dictionary
    :param analysis_result: AnalystResult to encode
    :return: dict
    """
    dictionary = analysis_result.__dict__
    convert = dictionary.pop('disabled_nodes')
    dictionary.__setitem__('disabled_nodes', list(convert))
    dictionary.__setitem__('_type', 'AnalysisResult')
    return dictionary

def decode_AnalysisResult(document: dict) -> AnalysisResult:
    """
    decodes dictionary in an AnalysisResult
    :param document: dictionary to decode
    :return: AnalysisResult
    """
    if document['_type'] == 'AnalysisResult':
        document.pop('_type')

        convert = document.pop('disabled_nodes')
        document.__setitem__('disabled_nodes', set(convert))

        result = AnalysisResult()
        result.__dict__ = document

        return result

def encode_StorageGenome(storage_genome: StorageGenome) -> dict:
    """
    encodes StorageGenome in a dictionary
    :param storage_genome: StorageGenome to encode
    :return: dict
    """
    dictionary = storage_genome.__dict__
    analysis_res = dictionary.pop('analysis_result')
    analysis_result = encode_AnalysisResult(analysis_res)
    dictionary.__setitem__('analysis_result', analysis_result)
    dictionary.__setitem__('_type', 'StorageGenome')
    return dictionary

def decode_StorageGenome(document: dict) -> StorageGenome:
    """
    decodes dictionary to StorageGenome
    :param document: dictionary to decode
    :return: StorageGenome
    """
    if document['_type'] == 'StorageGenome':
        document.pop('_type')
        analysis_result = decode_AnalysisResult(document.pop('analysis_result'))
        document.__setitem__('analysis_result', analysis_result.__dict__)
        storage_genome = StorageGenome()
        storage_genome.__dict__ = document
        return storage_genome

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