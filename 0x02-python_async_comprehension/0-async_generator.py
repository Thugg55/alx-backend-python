#usr/bin/env python3
"""asynchronous definition"""

import asyncio
import random


aync def async_generator():
    for _in range(10):
        await asyncio.sleep(1)
        yield random.uniform(0, 10)
