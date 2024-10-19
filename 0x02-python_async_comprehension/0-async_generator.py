#usr/bin/env python3
"""asynchronous definition"""

import asyncio
import random
from typing import Generator 


async def async_generator() -> Generator[float, None, None]:
    """
     Asynchronous generator function that yields a random float between 0 and 10
    after a one second delay for a total of 10 iterations.
    """
    for _in range(10):
        await asyncio.sleep(1)
        yield random.uniform(0, 10)
