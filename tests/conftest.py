import asyncio
import os
from typing import Iterator

import pytest
from dotenv import load_dotenv

load_dotenv('testing.env', override=True)

@pytest.fixture(scope="module")
def event_loop() -> Iterator[asyncio.AbstractEventLoop]:
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

