# -*- coding: utf-8 -*-
from os.path import abspath, dirname, join as path_join
from setuptools import setup

CURDIR = abspath(dirname(__file__))

# get VERSION number
exec(compile(open('src/ImageHorizonLibrary/version.py', "rb").read(), 'src/ImageHorizonLibrary/version.py', 'exec'))

KEYWORDS = ('imagerecognition gui robotframework testing testautomation '
            'acceptancetesting atdd bdd')

SHORT_DESC = ('Cross-platform Robot Framework library for GUI automation '
              'based on image recognition')

with open(path_join(CURDIR, 'README.rst'), 'r') as readme:
    LONG_DESCRIPTION = readme.read()

CLASSIFIERS = '''
Development Status :: 5 - Production/Stable
Programming Language :: Python :: 3 :: Only
Operating System :: OS Independent
Topic :: Software Development :: Testing
License :: OSI Approved :: MIT License
'''.strip().splitlines()

setup(name='robotframework-imagehorizonlibrary',
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
      package_dir={'': 'src'},
      keywords=KEYWORDS,
      classifiers=CLASSIFIERS,
      version=VERSION,
      description=SHORT_DESC,
      long_description=LONG_DESCRIPTION)
