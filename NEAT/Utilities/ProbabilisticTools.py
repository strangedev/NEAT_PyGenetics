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

    abs_probability = sum([s[1] for s in weighted_sample])
    object_bound_mapper = []
    lower_bound = 0

    random.seed()

    for sample in weighted_sample:

        obj = sample[0]
        probability = sample[1]

        bound_offset = probability / abs_probability
        upper_bound = lower_bound + bound_offset
        object_bound_mapper.append((obj, lower_bound, upper_bound))

        lower_bound = upper_bound

    x = random.random()

    for interval in object_bound_mapper:

        lower_bound = interval[1]
        upper_bound = interval[2]

        if (lower_bound < x) and (x <= upper_bound):
            return interval[0]

    return object_bound_mapper[-1][0]

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
    pass