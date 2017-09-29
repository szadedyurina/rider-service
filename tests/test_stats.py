from unittest import TestCase
from ..api.stats import Stats

class TestDistance(TestCase):

    check_values = {(27.538714, 53.896788, 27.576666, 53.930659): 4.513,
                    (27.538714, 53.896788, 27.538714, 53.896788): 0.0,
                    (0.0, 0.0, 0.0, 0.0): 0.0,
                    (0.0, 0.0, 0.0, 1.0): 111.2,
                    (0.0, 0.0, 1.0, 0.0): 111.2}

    symmentry_values = ((0.0, 0.0, 1.0, 1.0),
                        (1.0, 1.0, 0.0, 0.0))

    identity_values = ((1.0, 1.0, 1.0, 1.0),
                       (1.0, 1.0, 1.0, 1.0))

    subadditivity_values = ((0.0, 0.0, 0.0, 2.0),
                            (0.0, 2.0, 2.0, 2.0),
                            (0.0, 0.0, 2.0, 2.0))


    def test_get_distance(self):

        for key, value in self.check_values.items():
            self.assertAlmostEqual(Stats.get_distance(key[0], key[1], key[2], key[3]), value, delta=0.1)

    def distance_symmetry_test(self):
        """
        Symmetry property test: dist(a,b) = dist(b,a)
        """
        self.assertEqual(Stats.get_distance(self.symmentry_values[0]), self.symmentry_values[1])

    def identity_test(self):
        """
        Identity property test: dist(a,a)=0
        """
        self.assertEqual(Stats.get_distance(self.identity_values[0], self.identity_values[1]))

    def subadditivity_test(self):
        """
        Subadditivity (triangle inequality) test
        """
        self.assertGreater(Stats.get_distance(self.subadditivity_values[2],
                                              self.subadditivity_values[0] + self.subadditivity_values[1]))


if __name__ == '__main__':
    unittest.main()