#!/usr/bin/env python

import io
import os
import re
from collections import OrderedDict

from setuptools import find_packages, setup


def get_version(package):
    with io.open(os.path.join(package, "__init__.py")) as f:
        pattern = r'^__version__ = [\'"]([^\'"]*)[\'"]'
        return re.search(pattern, f.read(), re.MULTILINE).group(1) # type: ignore


setup(
    name="easy-logstash",
    version=get_version("easy_logstash"),
    license="MIT",
    description="A easy way to handle logs with logstash.",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author="Bang Phan (ptbang)",
    author_email="ptbang@gmail.com",
    maintainer="Bang Phan",
    url="https://github.com/ptbang/Easy-Logstash",
    project_urls=OrderedDict((("Documentation", "https://github.com/ptbang/Easy-Logstash"),)),
    packages=find_packages(exclude=["test*"]),
    install_requires=[
        "python-logstash-async>=2.5",
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    keywords="logstash logging async easy simple",
    zip_safe=False,
    include_package_data=True,
)
