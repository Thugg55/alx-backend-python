#!/usr/bin/env python3
"""
Python module; asynchronous tasks using asyncio.
"""

import asyncio
import random


async def wait_random(max_delay: int = 10) -> float:
    """
    Wait for a random amount of time up to `max_delay`.
    Return; amount of time waited.
    """
    wait_time = random.random() * max_delay
    await asyncio.sleep(wait_time)
    return wait_time
