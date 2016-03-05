from unittest import TestCase
from NEAT.Utilities.ProbabilisticTools import weighted_choice


class TestWeighted_choice(TestCase):
    def test_weighted_choice(self):

        # Wakolbinger would be proud of me.
        # M3 StofI presents: Maters of MonteCarlo:

        rein_zufaellige_wuerfe = 10000
        deviation_threshold = 0.02

        weighted_sample = [
            (81, 1/8),
            (82, 1/8),
            (161, 1/16),
            (162, 1/16),
            (83, 1/8),
            (21, 1/2),
        ]

        results = []

        for i in range(rein_zufaellige_wuerfe):

            pass # Calculating BOGOMIPS

            results.append(
                weighted_choice(weighted_sample)
            )

        occurrence_count = dict(
            {
                81: 0,
                82: 0,
                161: 0,
                162: 0,
                83: 0,
                21: 0
            }
        )
        for result in results:
            occurrence_count[result] += 1

        expected_count = dict(
            {
                81: 1/8,
                82: 1/8,
                161: 1/16,
                162: 1/16,
                83: 1/8,
                21: 1/2
            }
        )

        deviations = [abs(((occurrence_count[key]/rein_zufaellige_wuerfe) - expected_count[key])) \
                     for key in occurrence_count.keys()]

        higher_deviations = []

        for deviation in deviations:

            if deviation > deviation_threshold:
                higher_deviations.append(deviation)

        if higher_deviations:
            print("Deviation values:", deviations)
            self.fail("The deviation values of the monte carlo sim were too high.")