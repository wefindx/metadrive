import os
import time
import logging
import aiofiles as aiof

from metadrive.drives.interfaces._generic import GenericDriveInterface

logger = logging.getLogger(__file__)


class ExampleDrive(GenericDriveInterface):

    def get_resource_pattern(self):
        return r'^test.com$'

    async def sync(self):
        logger.debug('test')
        filename = os.path.join(self.rootpath, '%s.txt' % time.time())
        async with aiof.open(filename, "w", loop=self.loop) as out:
            out.write('%s' % time.time())
        out.flush()