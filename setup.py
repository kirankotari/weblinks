from setuptools import setup, find_packages
from os import path
from io import open

version = "1.1.0"

# setup file path
here = path.abspath(path.dirname(__file__))
reqs = []

# reading README.md, change if needed
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

with open(path.join(here, 'requirements.txt'), encoding='utf-8')as f:
    read_lines = f.readlines()
    reqs = [ each.strip() for each in read_lines]

setup(
    name='weblinks',
    version=version,
    description="Wanted to fetch the links from web and filter them using substring, a file extentions",
    long_description = long_description,
    long_description_content_type = 'text/markdown',
    url = 'https://github.com/kirankotari/weblinks',
    author = 'Kiran Kumar Kotari',
    author_email = 'kirankotari@live.com',

    # Un-comment to enable command line feature
    entry_points={
    	'console_scripts': [
    		'weblinks = weblinks.weblinks:main'
    	],
    },

    install_requires=reqs,
    classifiers = [ 
        # Choose the classifiers at https://pypi.org/classifiers/
        # Python Package Development Status. 
        'Development Status :: 5 - Production/Stable',
        # Most common <development-status> are: 
        # 3 - Alpha
        # 4 - Beta
        # 5 - Production/Stable

        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: Apache Software License', 
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
        ],
    keywords = 'weblinks getlinks web-links get-links fetch-links',
    packages = find_packages(where='.', exclude=['tests']),
    include_package_data=True,
)