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

    identity_values = {(1.0, 1.0, 1.0, 1.0): 0.0}

    subadditivity_values = ((0.0, 0.0, 0.0, 2.0),
                            (0.0, 2.0, 2.0, 2.0),
                            (0.0, 0.0, 2.0, 2.0))


    def test_get_distance(self):

        for key, value in self.check_values.items():
            self.assertAlmostEqual(Stats.get_distance(key[0], key[1], key[2], key[3]), value, delta=0.1)

    def test_distance_symmetry(self):
        """
        Symmetry property test: dist(a,b) = dist(b,a)
        """
        coord1 = self.symmentry_values[0]
        coord2 = self.symmentry_values[1]
        self.assertEqual(Stats.get_distance(coord1[0], coord1[1], coord1[2], coord1[3]),
                         Stats.get_distance(coord2[0], coord2[1], coord2[2], coord2[3]))

    def test_identity(self):
        """
        Identity property test: dist(a,a)=0
        """
        for key, value in self.identity_values.items():
            self.assertEqual(Stats.get_distance(key[0], key[1], key[2], key[3]), value)


    def test_subadditivity(self):
        """
        Subadditivity (triangle inequality) test
        """
        coord1 = self.subadditivity_values[0]
        coord2 = self.subadditivity_values[1]
        coord3 = self.subadditivity_values[2]
        self.assertLess(Stats.get_distance(coord3[0], coord3[1], coord3[2], coord3[3]),
                           Stats.get_distance(coord1[0], coord1[1], coord1[2], coord1[3])
                           + Stats.get_distance(coord2[0], coord2[1], coord2[2], coord2[3]))


if __name__ == '__main__':
    unittest.main()