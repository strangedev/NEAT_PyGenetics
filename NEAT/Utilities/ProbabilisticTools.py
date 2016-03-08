from typing import List, Tuple
import random

def weighted_choice(
        weighted_sample: List[Tuple[object, float]]
) -> object:
    """
    Chooses an object from a list of possible outcomes,
    possible outcomes are weighted by their probabilities of being chosen.
    :param weighted_sample: List of Tuples: (outcome, probability)
    :return: The chosen outcome
    """
    return weighted_choice_range(weighted_sample, 1)[0]

def weighted_choice_range(
        weighted_sample: List[Tuple[object, float]],
        count: int
) -> List[object]:
    """
    Chooses a number of objects from a list of possible outcomes,
    possible outcomes are weighted by their probabilities of being chosen.
    :param weighted_sample: List of Tuples: (outcome, probability)
    :param count: Amount of outcomes to choose
    :return: The chosen outcomes
    """
    abs_probability = sum([s[1] for s in weighted_sample])
    object_bound_mapper = dict({})
    lower_bound = 0

    random.seed()

    for sample in weighted_sample:

        obj = sample[0]
        probability = sample[1]

        bound_offset = probability / abs_probability
        upper_bound = lower_bound + bound_offset
        object_bound_mapper[(lower_bound, upper_bound)] = obj

        lower_bound = upper_bound

    random_draws = [random.random() for _ in range(count)]
    results = []

    for lower, upper in object_bound_mapper.keys():

        for x in random_draws:

            if (lower < x) and (x <= upper):
                results.append(object_bound_mapper[(lower, upper)])

    return results