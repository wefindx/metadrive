# Copyright (c) 2018 WeFindX Foundation, CLG.
# All Rights Reserved.
from setuptools import find_packages, setup

try:
    import pypandoc
    LONG_DESCRIPTION = pypandoc.convert_file('README.md', 'rst')
except ImportError:
    LONG_DESCRIPTION = 'Integration of controllers to drive tools.'


setup(
    name='metadrive',
    version='1.4.26',
    description='Integration of controllers to drive tools.',
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    url='https://gitlab.com/wefindx/metadrive',
    author='Mindey',
    author_email='mindey@qq.com',
    license='Apache 2.0',
    packages=find_packages(exclude=['docs', 'tests*']),
    install_requires=[
        'deprecated==1.2.5',
        'click==7.0',
        'fusepy==3.0.1',
        'tqdm==4.31.1',
        'yolk3k==0.9',  # TODO
        'metatype',
        'metawiki',
        'metaform',
        'typology',

        # 'selenium==3.141.0', # for _selenuim
        # 'xarray==0.12.1', # for _xarray
    ],
    extras_require={
        'test': ['coverage', 'pytest', 'pytest-cov'],
    },
    zip_safe=False,
    entry_points={
        'console_scripts': [
            'connect=metadrive.cli:connect'
        ],
    },
    package_data={
        'metadrive':
            []
    }
)
