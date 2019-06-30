class AbstractDriver:
    def __init__(self, loop, resource, root):
        self.loop = loop
        self.resource = resource
        self.root = root

    async def sync(self):
        raise NotImplementedError
