# Copyright (c) 2018 WeFindX Foundation, CLG.
# All Rights Reserved.

import os
from setuptools import find_packages, setup

LONG_DESCRIPTION = 'Integration of controllers to drive tools.'


setup(
    name='metadrive',
    version='1.4.34',
    description='Integration of controllers to drive tools.',
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    url='https://gitlab.com/wefindx/metadrive',
    author='Mindey',
    author_email='mindey@qq.com',
    license='Apache 2.0',
    packages = find_packages(exclude=['docs', 'tests*']),
    install_requires=[
        'Deprecated==1.2.5',
        'fusepy==3.0.1',
        # 'PyGithub==1.43.7',
        # 'pygithub3==0.5.1',
        'aiofiles==0.4.0',
        'apiage==0.1.4',
        'asyncio==3.4.3',
        'bs4==0.0.1',
        # 'celery==5.2.2',
        'click==7.1.2',
        # 'feedparser==5.2.1',
        'gitpython==2.1.11',
        'gpgrecord==0.0.4',
        'ipython==7.3.0',
        'jinja2==2.11.3',
        'metatype',
        'metawiki',
        'metaform',
        'paramiko==2.10.1',
        'pyautogui==0.9.42',
        'pymongo==3.7.2',
        'pysocks==1.6.8',
        'pytest==4.4.1',
        'python-dateutil==2.8.0',
        'python3-xlib==0.15',
        'requests==2.28.1',
        'selenium==3.141.0',
        'selenium-wire==2.1.1',
        'slumber==0.7.1',
        'Sphinx==2.0.1',
        'tqdm==4.31.1',
        'typology',
        'yolk3k==0.9',
        'xarray==0.12.1',
        'urllib3==1.26.5' # not sure if necessary
    ],
    extras_require = {
        'test': ['coverage', 'pytest', 'pytest-cov'],
    },
    zip_safe=False,
    entry_points = {
        'console_scripts': [
            'drive=metadrive.cli:connect'
        ],
    },
    package_data = {
        'metadrive':
            []
    }
)
