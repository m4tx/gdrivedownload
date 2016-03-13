from setuptools import setup
from codecs import open
from os import path

base_path = path.abspath(path.dirname(__file__))

with open(path.join(base_path, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
        name='gdrivedownload',
        version='1.0.1',
        description='Simple script that downloads all files from given '
                    'Google Drive directory',
        long_description=long_description,
        url='https://github.com/m4tx/gdrivedownload',

        author='Mateusz Maćkowski',
        author_email='m4tx@m4tx.pl',
        license='MIT',

        classifiers=[
            'Development Status :: 5 - Production/Stable',
            'Environment :: Console',
            'Intended Audience :: End Users/Desktop',
            'Topic :: Software Development :: Build Tools',
            'License :: OSI Approved :: MIT License',
            'Natural Language :: English',
            'Operating System :: OS Independent',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.2',
            'Programming Language :: Python :: 3.3',
            'Programming Language :: Python :: 3.4',
            'Programming Language :: Python :: 3.5',
            'Topic :: Internet :: WWW/HTTP',
            'Topic :: Utilities'
        ],

        keywords='google drive api batch download',
        py_modules=['gdrivedownload'],
        install_requires=['google-api-python-client>=1.5.0,<2'],
        entry_points={
            'console_scripts': [
                'gdrivedownload=gdrivedownload:main',
            ],
        },
)
