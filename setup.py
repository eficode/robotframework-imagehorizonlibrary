from setuptools import setup

setup(name='ImageHorizonLibrary',
      version='0.1',
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