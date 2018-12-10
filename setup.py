# Copyright (c) 2018 WeFindX Foundation, CLG.
# All Rights Reserved.

from setuptools import find_packages, setup

with open('README.md', 'r') as f:
    long_description = f.read()

setup(
    name='metadrive',
    version='0.6.6',
    description='Integration of controllers to drive tools.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://gitlab.com/wefindx/metadrive',
    author='Mindey',
    author_email='mindey@qq.com',
    license='MIT',
    packages = find_packages(exclude=['docs', 'tests*']),
    install_requires=[
        'gpgrecord',
        'metawiki',
        'metaform',
        'requests',
        'apiage',
        'paramiko',
        'selenium',
        'slumber',
        'feedparser',
        'click',
        'python-dateutil',
        'bs4',
        'pyautogui',
        'python3-xlib',
        'pysocks',
        'starlette',
        'uvicorn',
        'graphene',
        # 'selendroid',
    ],
    extras_require = {
        'test': ['coverage', 'pytest', 'pytest-cov'],
    },
    zip_safe=False,
    entry_points = {
        'console_scripts': [
            'harvest=metadrive.cli:harvest',
            'provide=metadrive.cli:provide'
        ],
    }
)
