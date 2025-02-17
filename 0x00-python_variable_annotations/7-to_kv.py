#!/usr/bin/env python3
"""
Complex types - string and int/float to tuple
Write typed-annotated function to_kv that takes str k and an int OR float v
Returns a tuple
"""

from typing import Callable, Iterator, Union, Optional, List, Tuple


def to_kv(k: str, v: Union[int, float]) -> Tuple[str, float]:
    """
    takes a string k and an int OR float v as arguments
    returns a tuple.
    """

    return (k, v**2)
