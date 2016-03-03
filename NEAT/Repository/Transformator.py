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
