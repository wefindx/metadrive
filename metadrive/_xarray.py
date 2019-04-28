import os
# import xarray
import pandas
import inspect
from metadrive import mixins


SUBTOOL = os.path.basename(__file__).split('.py')[0]


class XarrayDrive:

    def __init__(self):
        self.desired_capabilities = {}
        self.metaname = ''
        self.df = None

    def read_csv(self, *args, **kwargs):
        self.df = pandas.read_csv(*args, **kwargs)


def get_drive(
        profile='default',
        porfiles_dir='.metadrive/sessions/_xarray',
        recreate_profile=False,
        proxies='default'):

    proxy = mixins.set_proxies(proxies)
    local = mixins.init_profile(profile, porfiles_dir, recreate_profile)

    drive = XarrayDrive()
    drive.subtool = SUBTOOL
    drive.profile = profile

    # LATER MOVE TO MIXIN
    drive.caller_module = inspect.getmodule(inspect.currentframe().f_back)

    return drive
