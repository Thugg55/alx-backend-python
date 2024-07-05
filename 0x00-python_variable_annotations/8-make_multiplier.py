#!/usr/bin/env python3
"""
Complex types - functions
Write typed-annotated function make_multiplier
takes float multiplier argument
Returns function that multiplies a float by a multipier
"""

from typing import Callable


def make_multiplier(multiplier: float) -> Callable[[float], float]:
    """
    Args:
        k (str)
        v (int or float)
    Return:
        (tuple): a tuple of k and square of v
    """
    def multiply(f: float) -> float:
        """
        Multiplies multiplier by f
        Args:
            f (float)
        Returns:
            (float)
        """
        return multiplier * f
    return multiply
