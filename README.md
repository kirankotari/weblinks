# Weblinks

[![License: Apache 2.0](https://img.shields.io/badge/License-Apache2-yellow.svg)](https://opensource.org/licenses/Apache-2.0)
[![pytest](https://github.com/kirankotari/weblinks/actions/workflows/pytest.yml/badge.svg)](https://github.com/kirankotari/weblinks/actions/workflows/pytest.yml)
![GitHub release (latest by date)](https://img.shields.io/github/v/release/kirankotari/weblinks)
[![Downloads](https://static.pepy.tech/personalized-badge/weblinks?period=total&units=international_system&left_color=grey&right_color=orange&left_text=pypi%20downloads)](https://pepy.tech/project/weblinks)
[![Downloads](https://static.pepy.tech/personalized-badge/weblinks?period=week&units=international_system&left_color=grey&right_color=orange&left_text=pypi%20downloads/week)](https://pepy.tech/project/weblinks)
![GitHub all releases](https://img.shields.io/github/downloads/kirankotari/weblinks/total?label=github%20downloads)
![GitHub top language](https://img.shields.io/github/languages/top/kirankotari/weblinks)
![GitHub issues](https://img.shields.io/github/issues/kirankotari/weblinks)
![GitHub pull requests](https://img.shields.io/github/issues-pr/kirankotari/weblinks)

- [Introduction](#introduction)
- [Installation and Downloads](#installation-and-downloads)
- [Usage](#usage)
- [License and Copyright](#license-and-copyright)
- [Author and Thanks](#author-and-thanks)

## Introduction

Weblinks, It get all links from a given website and we can apply filters on top of it to get desired results, when you are good you can start downloading them with `-d` flag.

TODO: many changes, add-ons need to update in full.!

In the library we are supporting plain webpages, authentication based webpages.

## Pre-req

A system need to have curl and python

## Docs

How to use weblinks?

```python

```
## Installation and Downloads

`pip install weblinks`

## Usage

```
usage: weblinks [-h] -w WEB [-u USERNAME] [-p PASSWORD] [-e EXT] [-d] [-v]
                   substring

positional arguments:
  substring             the sub-string in the links

optional arguments:
  -h, --help            show this help message and exit
  -w WEB, --web WEB     the website
  -u USERNAME, --username USERNAME
                        web login username
  -p PASSWORD, --password PASSWORD
                        web login password
  -e EXT, --ext EXT     file extention
  -d, --download        download links
  -v, --verbosity
```

## License and Copyright

- weblinks is licensed [Apache 2.0](https://opensource.org/licenses/Apache-2.0) 2022

## Author and Thanks

Weblinks was developed by [Kiran Kumar Kotari](https://github.com/kirankotari)
