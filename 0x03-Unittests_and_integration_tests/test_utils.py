#!/usr/bin/python3
"""first unit test for
   utils.access_nested_map
"""

import unittest
from parameterized import parameterized

# to access utils.access_nested_map
from utils import access_nested_map


class TestAccessNestedMap(unittest.TestCase):
    """Implemented a class or nested map test"""

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        """implement the defined unction"""
        self.assertEqual(access_nested_map(nested_map, path), expected)


if __name__ == '__main__':
    unittest.main()
