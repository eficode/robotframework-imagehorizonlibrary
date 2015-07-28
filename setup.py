# -*- coding: utf-8 -*-s
from setuptools import setup

execfile('src/ImageHorizonLibrary/version.py')

setup(name='ImageHorizonLibrary',
    version=VERSION,
    description='ImageHorizonLibrary',
    author='Eficode Oy',
    author_email='info@eficode.com',
    url='https://github.com/Eficode/robotframework-imagehorizonlibrary',
    license='MIT',
    install_requires=[
      'robotframework>=2.8',
      'pyautogui>=0.9.30'
    ],
    packages=[
      'ImageHorizonLibrary',
      'ImageHorizonLibrary.interaction',
      'ImageHorizonLibrary.recognition',
    ],
    package_dir = {'': 'src'}
)