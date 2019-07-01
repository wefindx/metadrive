class AbstractDrive:
    # regexp pattern
    resource_pattern = None

    def __init__(self, loop, resource, rootpath):
        self.loop = loop
        self.resource = resource
        self.rootpath = rootpath

    async def sync(self):
        raise NotImplementedError
