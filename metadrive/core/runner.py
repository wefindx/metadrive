import asyncio
import os
import signal
from concurrent.futures import ProcessPoolExecutor

from metadrive import settings
from metadrive.core.driver import get_driver
from metadrive.core.mount import mount


class MetaDriveRunner:
    def __init__(self, resource, mountpoint=None, user=None, period=900):
        self.resource = resource
        self.mountpoint = mountpoint
        self.user = user or 'default'
        self.period = period

        if self.mountpoint is None:
            self.mountpoint = os.path.join(
                settings.MOUNT_DIR,
                resource,
                self.user
            )

        self.root = os.path.join(
            settings.DATA_DIR,
            resource,
            self.user
        )

        self.loop = asyncio.get_event_loop()
        self.executor = ProcessPoolExecutor()
        self.loop.add_signal_handler(signal.SIGINT, self.shutdown)

    async def mount_filesystem(self):
        await self.loop.run_in_executor(
            self.executor,
            mount,
            self.root,
            self.mountpoint
        )

    async def sync_by_driver(self):
        driver_cls = await get_driver(self.resource)
        driver_obj = driver_cls(self.loop, self.resource, self.root)
        await driver_obj.sync()

    def run(self):
        self.loop.create_task(self.mount_filesystem())
        self.loop.create_task(self.sync_by_driver())
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
