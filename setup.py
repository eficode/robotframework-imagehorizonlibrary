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
          # Version 10 is not fully compatible (https://stackoverflow.com/questions/76616042/attributeerror-module-pil-image-has-no-attribute-antialias)
          'matplotlib',
          'Pillow==9.5.0',
          'PyScreeze==0.1.29',
          'pyautogui>=0.9.30',
          #'scikit-image@ file://
          #'scikit-image==0.22.0 @ https://files.pythonhosted.org/packages/ce/d0/a3f60c9f57ed295b3076e4acdb29a37bbd8823452562ab2ad51b03d6f377/scikit_image-0.22.0-cp311-cp311-win_amd64.whl',
          # scikit-image 0.19 can't be used yet - regression bug
          # (reference images get an unexplainable white 1px border)
          #'scikit-image==0.18.3',
          'scikit-image==0.22.0',
          #'matplotlib==3.4.3'
      ],
      packages=[
          'ImageHorizonLibrary',
          'ImageHorizonLibrary.interaction',
          'ImageHorizonLibrary.recognition',
          'ImageHorizonLibrary.recognition.ImageDebugger'
      ],
      package_dir={'': 'src'},
      keywords=KEYWORDS,
      classifiers=CLASSIFIERS,
      version=VERSION,
      description=SHORT_DESC,
      long_description=LONG_DESCRIPTION)
