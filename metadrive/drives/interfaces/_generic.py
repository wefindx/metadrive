class GenericDriveInterface:
    def __init__(self, loop, resource, rootpath):
        self.loop = loop
        self.resource = resource
        self.rootpath = rootpath

    def get_resource_pattern(self):
        raise NotImplementedError

    async def sync(self):
        raise NotImplementedError
