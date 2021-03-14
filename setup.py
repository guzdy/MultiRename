# ！/usr/bin/env python
# -*- coding= utf-8 -*-

from setuptools import setup, find_packages


setup(
    name='mtrn',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'mtrn = src.multiRename:menu1'
        ]
    },
    install_requires=[
        'pillow',
    ],
    license='MIT',
    author='guzdy',
    author_email='guz.jin@gmail.com',
    description='批量重命名软件'
)
