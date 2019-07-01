import asyncio
import os
import signal
import importlib
import re
import logging
import sys
from concurrent.futures import ProcessPoolExecutor

from metadrive import settings
from metadrive.core.mount import mount

logger = logging.getLogger(__file__)


class MetaDriveRunner:
    def __init__(self, resource, mountpoint=None, session=None):
        self.resource = resource
        self.session = session or 'default'
        self.mountpoint = mountpoint or os.path.join(
            settings.MOUNT_DIR,
            '{}:{}'.format(self.resource, self.session)
        )
        self.rootpath = os.path.join(
            settings.DATA_DIR,
            '{}:{}'.format(self.resource, self.session)
        )

        self.loop = asyncio.get_event_loop()
        self.executor = ProcessPoolExecutor()
        self.loop.add_signal_handler(signal.SIGINT, self.shutdown)

        try:
            os.mkdir(self.rootpath)
        except FileExistsError:
            pass

        self.drive = None
        for drive in settings.DRIVES:
            module_name, class_name = drive.split(':')
            module = importlib.import_module(module_name)
            drive_class = getattr(module, class_name)
            if re.match(drive_class.get_resource_pattern(), self.resource):
                self.drive = drive_class(
                    self.resource,
                    self.rootpath
                )
                break
        if self.drive is None:
            logger.warning('No drive for resource %s', self.resource)
            sys.exit(0)

    async def _mount_filesystem(self):
        await self.loop.run_in_executor(
            self.executor,
            mount,
            self.mountpoint,
            self.drive.__class__,
            self.resource,
            self.rootpath,
        )

    async def _sync_drive(self):
        await self.drive.sync()

    def run(self):
        self.loop.create_task(self._mount_filesystem())
        self.loop.create_task(self._sync_drive())
        self.loop.run_forever()

        pending = asyncio.Task.all_tasks(loop=self.loop)
        group = asyncio.gather(*pending)
        self.loop.run_until_complete(group)
        self.loop.close()

    def shutdown(self):
        self.executor.shutdown()
        # for task in asyncio.Task.all_tasks():
        #     task.cancel()
        self.loop.stop()
