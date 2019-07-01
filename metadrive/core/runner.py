import asyncio
import os
import signal
import importlib
import re
import logging
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

        self.drives = []
        for drive in settings.DRIVES:
            module_name, class_name = drive.split(':')
            module = importlib.import_module(module_name)
            drive_class = getattr(module, class_name)
            self.drives.append(
                drive_class(self.loop, self.resource, self.rootpath)
            )

    async def _get_drive(self):
        for drive in self.drives:
            if re.match(drive.get_resource_pattern(), self.resource):
                return drive
        logger.warning('No drive for resource %s', self.resource)

    async def _mount_filesystem(self):
        await self.loop.run_in_executor(
            self.executor,
            mount,
            self.rootpath,
            self.mountpoint
        )

    async def _sync_by_driver(self):
        drive = await self._get_drive()
        if drive:
            await drive.sync()

    def run(self):
        self.loop.create_task(self._mount_filesystem())
        self.loop.create_task(self._sync_by_driver())
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
