import os
from pathlib import Path

HOME = str(Path.home())
CONFIG_DIR = os.path.join(HOME, '.metadrive')
DATA_DIR = os.path.join(CONFIG_DIR, 'data')
MOUNT_DIR = os.path.join(HOME, 'Sites')
