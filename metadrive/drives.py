import os
from metadrive.config import (
    INSTALLED,
    API_HOST,
    API_PORT,
    SESSIONS_DIR,
    SUBTOOLS
)
from metadrive.utils import find_drivers
from metadrive import utils

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

def next_string(s):
    a1 = range(65, 91)  # capital letters
    a2 = range(97, 123) # letters
    a3 = range(48, 58)  # numbers
    char = ord(s[-1])
    for a in [a1, a2, a3]:
        if char in a:
            if char + 1 in a:
                return s[:-1] + chr(char + 1)
            else:
                ns = next_string(s[:-1]) if s[:-1] else chr(a[0])
                return ns + chr(a[0])

def get(driver_or_drive, latest_or_new=True):
    if driver_or_drive in ACTIVE:
        return ACTIVE[driver_or_drive]

    if ':' in driver_or_drive:
        driver, drive_id = driver_or_drive.split(':',1)
        drive = driver_or_drive
    else:
        driver = driver_or_drive
        drive_id = None
        drive = None

    ndriver = driver.replace('-', '_')
    package = utils.ensure_driver_installed(driver_name='pypi:{}'.format(ndriver))
    module = __import__(package)

    drives = list(zip(*all()))[1]
    ids = sorted([d.split(':',1)[-1] for d in drives if ':' in d])

    if drive in drives:
        drive_obj = module.get_driver(profile=drive)
    elif drive is not None:
        drive_obj = module.get_driver(profile=drive)
    else:
        if ids:
            i = ids[-1]
        else:
            i = '0'

        drive = '{}:{}'.format(driver, next_string(i))
        drive_obj = module.get_driver(profile=drive)

    ACTIVE[drive] = drive_obj

    drive_obj.drive_id = drive

    return drive_obj


def quit(drive):
    if drive in ACTIVE:
        ACTIVE[drive].quit()
        del ACTIVE[drive]
