#!/usr/bin/env python3
"""
Complex types - mixed list
Write typed-annotated function sum_mixed_list
get mixed list integers and floats
Returns sum as float
"""

from typing import Union, List


def sum_mixed_list(mxd_lst: List[Union[int, float]]) -> float:
    """  returns sum as a float. """
    return float(sum(mxd_lst))
