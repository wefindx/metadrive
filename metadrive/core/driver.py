import logging
import os
import time

import aiofiles as aiof

logger = logging.getLogger(__file__)


class Driver:
    def __init__(self, loop, resource, root):
        self.loop = loop
        self.resource = resource
        self.root = root

    async def sync(self):
        raise NotImplementedError


class TestDriver(Driver):

    async def sync(self):
        logger.debug('test')
        filename = os.path.join(self.root, '%s.txt' % time.time())
        async with aiof.open(filename, "w", loop=self.loop) as out:
            out.write('%s' % time.time())
        out.flush()


async def get_driver(resource):
    # TODO identify driver by resource
    return TestDriver
