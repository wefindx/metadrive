import os
import imp
from pathlib import Path
import configparser
import requests
import gpgrecord
config = configparser.ConfigParser()

INSTALLED = imp.find_module('metadrive')[1]

HOME = str(Path.home())
DEFAULT_LOCATION = os.path.join(HOME,'.metadrive')
CONFIG_LOCATION = os.path.join(DEFAULT_LOCATION, 'config')
CREDENTIALS_DIR = os.path.join(DEFAULT_LOCATION, '-/+')
SESSIONS_DIR = os.path.join(DEFAULT_LOCATION, 'sessions')
DATA_DIR = os.path.join(DEFAULT_LOCATION, 'data')

SUBTOOLS = [
    fn.rsplit('.py')[0]
    for fn in os.listdir(INSTALLED)
    if fn.startswith('_') and fn.endswith('.py') and not fn == '__init__.py'
]


def ENSURE_SESSIONS():
    if not os.path.exists(SESSIONS_DIR):
        os.makedirs(SESSIONS_DIR)

    for subtool in SUBTOOLS:
        subtool_profiles_path = os.path.join(SESSIONS_DIR, subtool)
        if not os.path.exists(subtool_profiles_path):
            if subtool != '__init__':
                os.makedirs(subtool_profiles_path)

ENSURE_SESSIONS()

def ENSURE_DATA():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

ENSURE_DATA()



if not os.path.exists(CONFIG_LOCATION):
    username = input("Type your GitHub username: ")

    config['GITHUB'] = {'USERNAME': username}
    config['API'] = {'HOST': '0.0.0.0', 'PORT': 7000}
    config['CONSOLE'] = {'HOST': '0.0.0.0', 'PORT': 7000}
    config['PROXIES'] = {'http': '', 'https': ''}
    config['DRIVERS'] = {'auto_upgrade': False}
    config['DRIVER_BACKENDS'] = {
        'CHROME': '/usr/bin/chromedriver' # e.g., or http://0.0.0.0:4444/wd/hub, etc.
    }

    with open(CONFIG_LOCATION, 'w') as configfile:
        config.write(configfile)

config.read(CONFIG_LOCATION)

GITHUB_USER = config['GITHUB']['USERNAME']
REPO_PATH = os.path.join(DEFAULT_LOCATION, '-')
DRIVERS_PATH = os.path.join(DEFAULT_LOCATION, 'drivers')
API_HOST= config['API']['HOST']
API_PORT= int(config['API']['PORT'])
CONSOLE_HOST= config['CONSOLE']['HOST']
CONSOLE_PORT= int(config['CONSOLE']['PORT'])
CHROME_DRIVER = config['DRIVER_BACKENDS']['CHROME']

if str(config['DRIVERS']['auto_upgrade']) == 'False':
    AUTO_UPGRADE_DRIVERS = False
elif str(config['DRIVERS']['auto_upgrade']) == 'True':
    AUTO_UPGRADE_DRIVERS = True
elif str(config['DRIVERS']['auto_upgrade']) == 'None':
    AUTO_UPGRADE_DRIVERS = None
else:
    AUTO_UPGRADE_DRIVERS = False


def ENSURE_REPO():

    while not requests.get('https://github.com/{}/-'.format(GITHUB_USER)).ok:
        input("Please, create repository named `-` on your GitHub. Type [ENTER] to continue... ")


    if os.path.exists(REPO_PATH):
        # git pull #
        os.system('cd {}; git pull'.format(REPO_PATH))
    else:
        # git clone #
        os.system('cd {}; git clone {}'.format(
            DEFAULT_LOCATION,
            'git@github.com:{}/-.git'.format(GITHUB_USER)))

    if not os.path.exists(CREDENTIALS_DIR):
        os.makedirs(CREDENTIALS_DIR)
        os.system("cd {}; git add .; git commit -m 'credentials (+)'; git push origin master".format(
            REPO_PATH
        ))

def ENSURE_GPG():
    config.read(CONFIG_LOCATION)
    if 'GPG' in config.keys():
        return config['GPG']['KEY']

    print('Choose your GPG key for encrypting credentials:')
    KEY_LIST = gpgrecord.list_recipients()

    for i, key in enumerate(KEY_LIST):
        print('{id}. {uid} {fingerprint}'.format(
            id=i+1,
            uid=key['uids'],
            fingerprint=key['fingerprint']
        ))

    i = int(input('Type key order in the list: ')) - 1

    GPG_KEY = KEY_LIST[i]['fingerprint']

    config['GPG'] = {'KEY': GPG_KEY}

    with open(CONFIG_LOCATION, 'w') as configfile:
        config.write(configfile)

    return GPG_KEY

def ENSURE_PROXIES():
    config.read(CONFIG_LOCATION)
    if 'PROXIES' in config.keys():
        return {key: 'socks5h://'+config['PROXIES'][key] or None
                for key in config['PROXIES'] if config['PROXIES'][key]}

    SOCKS5 = input('Type-in default socks5 proxy  (e.g., 127.0.0.1:9999) (leave emtpy to default to direct connections) [ENTER]: ')

    config['PROXIES'] = {
        'http': SOCKS5,
        'https': SOCKS5
    }

    with open(CONFIG_LOCATION, 'w') as configfile:
        config.write(configfile)

    return {key: 'socks5h://'+config['PROXIES'][key] or None
            for key in config['PROXIES'] if config['PROXIES'][key]}
