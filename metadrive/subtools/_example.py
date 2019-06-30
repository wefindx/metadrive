import os
import time
import logging
import aiofiles as aiof

from metadrive.core.driver import AbstractDriver

logger = logging.getLogger(__file__)


class ExampleDriver(AbstractDriver):

    async def sync(self):
        logger.debug('test')
        filename = os.path.join(self.root, '%s.txt' % time.time())
        async with aiof.open(filename, "w", loop=self.loop) as out:
            out.write('%s' % time.time())
        out.flush()
