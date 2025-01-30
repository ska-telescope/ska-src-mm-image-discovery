#!/usr/bin/env python

import glob

from setuptools import setup

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

with open('VERSION') as f:
    version = f.read()

data_files = [
    ('etc', glob.glob('etc/*')),
]
scripts = glob.glob('bin/*')

setup(
    name='ska_src_mm_image_discovery_api',
    version=version,
    description='The mm-image-discovery API for SRCNet.',
    url='',
    author='rob barnsley',
    author_email='rob.barnsley@skao.int',
    packages=['ska_src_mm_image_discovery_api.rest', 'ska_src_mm_image_discovery_api.common', 'ska_src_mm_image_discovery_api.client',
              'ska_src_mm_image_discovery_api.models'],
    package_dir={'': 'src'},
    data_files=data_files,
    scripts=scripts,
    include_package_data=True,
    install_requires=requirements,
    classifiers=[]
)
