
import asyncio
import os


class GenericDriveInterface:
    def __init__(self, resource, rootpath):
        self.loop = asyncio.get_event_loop()
        self.resource = resource
        self.rootpath = rootpath

    @classmethod
    def get_resource_pattern(cls):
        raise NotImplementedError

    async def sync(self):
        raise NotImplementedError

    def read(self, path, length, offset, fh):
        os.lseek(fh, offset, os.SEEK_SET)
        return os.read(fh, length)

    def write(self, path, buf, offset, fh):
        os.lseek(fh, offset, os.SEEK_SET)
        return os.write(fh, buf)
