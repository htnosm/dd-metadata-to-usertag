#!/usr/bin/env python

from setuptools import setup, find_packages

#def _requires_from_file(filename):
#    return open(filename).read().splitlines()

setup(
  name="dd_add_metadata",
  version="0.1",
  packages=find_packages(),
  #install_requires=_requires_from_file('requirements.txt'),
  install_requires=[
    "datadog",
    "PyYAML",
  ],
  python_requires=">=3.8",
  include_package_data=True,
  package_data={
    "dd_add_metadata":["include_keys.yml"]
  },
  entry_points={
    'console_scripts':
      'dd_add_metadata = dd_add_metadata.dd_add_metadata:main'
  }
)
