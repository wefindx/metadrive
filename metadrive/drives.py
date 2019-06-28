import os

import pkg_resources

from metadrive import utils
from metadrive.config import INSTALLED, SESSIONS_DIR, SUBTOOLS
from metadrive.utils import find_drivers

# This package manages what profiles are created, and actually the sessions on disk,
# rather than active sessions on API.

ACTIVE = {}

def all():
    '''
    second coordinate uniquely identifies drives
    second item in tuples uniquely identifies drives, without the first.
    '''
    drives_map = []

    for subtool in SUBTOOLS:
        subtool_dir = os.path.join(SESSIONS_DIR,subtool)

        for drive_dir in os.listdir(subtool_dir):
            drives_map.append((subtool, drive_dir, 'ALIVE' if ACTIVE.get(drive_dir) else 'DEAD'))

    return drives_map


def get(driver_or_drive, interactive=False):

    if driver_or_drive in ACTIVE:
        return ACTIVE[driver_or_drive]

    if ':' in driver_or_drive:
        driver, drive_id = driver_or_drive.split(':',1)
        drive = driver_or_drive
    else:
        driver = driver_or_drive
        drive = None
        drive_id = None

    ndriver = driver.replace('-', '_')
    package = utils.ensure_driver_installed(driver_name='pypi:{}'.format(ndriver))
    module = __import__(package)

    d = all()
    drives = list(zip(*d))[1] if d else []

    ids = sorted([d.split(':',1)[-1] for d in drives if ':' in d])

    if drive in drives:
        drive_obj = module.get_drive(profile=drive)
    elif drive is not None:
        if os.name in ['nt']:
            drive_obj = module.get_drive(profile=drive.replace(':', '__'))
        else:
            drive_obj = module.get_drive(profile=drive)
    else:
        if ids:
            i = ids[-1]
        else:
            i = '0'

        import inspect
        if interactive and 'interactive' in inspect.getfullargspec(module._login).args:
            drive_obj = module._login(interactive=interactive)
            drive = drive_obj.profile.rsplit(':', 1)[-1]
            drive = '{}:{}'.format(driver, drive)
        else:
            drive = '{}:{}'.format(driver, 'default')
            drive_obj = module.get_drive(profile=drive)

    ACTIVE[drive] = drive_obj

    drive_obj.drive_id = drive
    driver_version = pkg_resources.require(ndriver)[0].version

    # TODO: refactor with api.py#creating-informative-drive
    drive_obj.spec = '{packman}::{driver}=={version}:{profile}.{namespace}'.format(
        packman='PyPI',
        driver=drive_obj.drive_id.split(':',1)[0], #.replace('-', '_'),
        version=driver_version,
        profile=drive_obj.drive_id.rsplit(':',1)[-1],
        namespace='api.',
        # namspace not present, because it's a drive, but we prepare based on drivers package convention, the .api.
        # then, in packages we only have to provide type(self).__name__, e.g.:
        # item['@'] = drive.spec + type(self).__name__
    )

    return drive_obj


def close(drive_obj):
    found = False
    for name, drive in ACTIVE.items():
        if drive == drive_obj:
            found = True
            break

    if found:
        drive_obj.quit()
        del ACTIVE[name]


def remove(drive_obj):
    drive_id = drive_obj.drive_id

    subtool = None
    for drive in all():
        if drive[1] == drive_id:
            subtool = drive[0]

    if subtool is not None:
        close(drive_obj)
        import shutil
        shutil.rmtree(os.path.join(SESSIONS_DIR, subtool, drive_id))
