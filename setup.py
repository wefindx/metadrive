# Copyright (c) 2018 WeFindX Foundation, CLG.
# All Rights Reserved.

from setuptools import find_packages, setup

with open('README.md', 'r') as f:
    long_description = f.read()

setup(
    name='drivers',
    version='0.0.1',
    description='Integration of controllers to drive tools.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/wefindx/drivers',
    author='Mindey',
    author_email='mindey@qq.com',
    license='MIT',
    packages = find_packages(exclude=['docs', 'tests*']),
    install_requires=[
    ],
    extras_require = {
        'test': ['coverage', 'pytest', 'pytest-cov'],
    },
    zip_safe=False
)
