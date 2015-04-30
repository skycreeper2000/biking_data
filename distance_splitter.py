
# coding: utf-8

# In[3]:

import unittest


def filter(alt_list):
    filtered = []
    compare = alt_list[0]

    for x, y in alt_list:
        if x < compare[0]:
            continue
        elif x >= compare[0]:
            filtered.append((x, y))
            compare = x, y

    print filtered
    return filtered


class TestFilters(unittest.TestCase):
    def test_nothing_to_remove(self):
        self.assertEqual(filter([(1, 2), (2, 2)]), [(1, 2), (2, 2)])

    def test_distance_decreases(self):
        self.assertEqual(filter([(1, 2), (2, 2), (3, 2), (2, 3), (1, 4)]), [(1, 2), (2, 2), (3, 2)])

    def test_distance_decreases_then_increases_again(self):
        self.assertEqual(filter([(1, 2), (2, 2), (3, 2), (2, 3), (1, 4), (4, 4), (5, 5)]),
                         [(1, 2), (2, 2), (3, 2), (4, 4), (5, 5)])

if __name__ == '__main__':
    unittest.main()
        





