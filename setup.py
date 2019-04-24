# !/usr/bin/python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name = "fastrequests",
    version = "1.0.0",
    keywords = ("pip", "requests","aiohttp", "spider"),
    description = "zjspider",
    long_description = "Encapsulate aiohttp as a framework for treating requests like but faster than requests",
    license = "MIT Licence",
    url = "https://github.com/ZJ1996-11/zjspider",
    author = "ZJ1996-11",
    author_email = "1209429223@qq.com",
    packages = find_packages(),
    include_package_data = True,
    platforms = "any",
    install_requires = ['aiohttp','lxml']
)
