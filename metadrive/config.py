import os
from pathlib import Path
import configparser
import requests
config = configparser.ConfigParser()

HOME = str(Path.home())
DEFAULT_LOCATION = os.path.join(HOME,'.metadrive')
CONFIG_LOCATION = os.path.join(DEFAULT_LOCATION, 'config')

if not os.path.exists(CONFIG_LOCATION):
    username = input("Type your GitHub username: ")

    config['GITHUB'] = {'USERNAME': username}

    with open(CONFIG_LOCATION, 'w') as configfile:
        config.write(configfile)

config.read(CONFIG_LOCATION)

GITHUB_USER = config['GITHUB']['USERNAME']

while not requests.get('https://github.com/{}/-'.format(GITHUB_USER)).ok:

    input("Please, create repository named `-` on your GitHub. Type [ENTER] to continue... ")

REPO_PATH = os.path.join(DEFAULT_LOCATION, '-')

if os.path.exists(REPO_PATH):
    # git pull #
    os.system('cd {}; git pull'.format(REPO_PATH))
else:
    # git clone #
    os.system('cd {}; git clone {}'.format(
        CONFIG_LOCATION,
        'git@github.com:{}/-.git'.format(GITHUB_USER)))
