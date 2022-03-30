from setuptools import setup, find_packages
from os import path
from io import open

# setup file path
here = path.abspath(path.dirname(__file__))
reqs = []

# reading README.md, change if needed
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()
# if no README.md exist then un-comment the below line
# long_description = '''<add-your-description-here>'''

# reading pre-requisits if any else comment the block
with open(path.join(here, 'requirements.txt'), encoding='utf-8')as f:
    read_lines = f.readlines()
    reqs = [ each.strip() for each in read_lines]

setup(
    name='weblinks',
    version='1.0',
    description="Wanted to fetch the links from web and filter them using substring, a file extentions",
    long_description = long_description,
    long_description_content_type = 'text/markdown',
    url = '<package-url or github-url>',
    author = '<author-name>',
    author_email='<author-email>',
    
    # Un-comment to enable command line feature
    entry_points={
    	'console_scripts': [
    		'weblinks = weblinks.weblinks:get'
    	],
    },

    install_requires=reqs,
    classifiers = [ 
        # Choose the classifiers at https://pypi.org/classifiers/

        # Python Package Development Status. 
        'Development Status :: 3 - Alpha',
        # Most common <development-status> are: 
        # 3 - Alpha
        # 4 - Beta
        # 5 - Production/Stable

        'Intended Audience :: <audience>',
        # Most common <audience> are:
        # Developers
        # Education
        # Manufacturing
        # Science/Research

        'Topic :: <package-for> :: <package-useage-at>',
        # In general <package-for> "Software Development" and <package-useage-at> "Build Tools"

        'License :: <license-approved-by> :: <license>', 
        # In general <license-approved-by> OSI Approved and <license> MIT License

        # Python version support all sub-version of 2 and 3
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',

        # Un-comment below if your package is for a special purpose
        # 'Framework :: <frame-work>',
        # 'Natural Language :: <language>',
        # 'Operating System :: <os-name>',
        # 'Programming Language :: <programming-language>',
        # 'Topic :: <topic>',
        ],
    keywords = '<package-keywords-seperated-by-space>',
    
    # add folder-names which need to be ignored under exclude=[]
    packages = find_packages(where='.', exclude=['tests', 'data']),
    include_package_data=True,
)