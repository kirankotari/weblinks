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
- [Pre-requisites](#pre-requisites)
- [Installation and Downloads](#installation-and-downloads)
- [Commands](#commands)
- [Docs](#docs)
- [Bug Tracker and Support](#bug-tracker-and-support)
- [License and Copyright](#license-and-copyright)
- [Author and Thanks](#author-and-thanks)


## Introduction

Weblinks, It get all links from a given website and we can apply filters on top of it to get desired results, when you are good you can start downloading them with `-d` flag.

In the library we are supporting plain webpages, authentication based webpages, proxy, authentication on proxy, etc. 

We also support storing the config in either local/global configuration, for best practise we suggest not to store your password, you get a prompt on runtime wher you can provide it.

## Pre-requisites

A system need to support **curl commands** and **python3**

## Installation and Downloads

```shell
pip install weblinks
```

## Commands

```shell
weblinks --help
```
```
usage: weblinks [-h] [-w WEB] [-s SUBSTRING] [-e EXT] [-d] [-u USERNAME]
                [-p PASSWORD] [-g] [-l] [-v] [--proxy PROXY]
                [--proxy-username PROXY_USERNAME]
                [--proxy-password PROXY_PASSWORD] [--version]

optional arguments:
  -h, --help            show this help message and exit
  -w WEB, --web WEB     the website
  -s SUBSTRING, --substring SUBSTRING
                        the sub-string in the links
  -e EXT, --ext EXT     file extention
  -d, --download        download links
  -u USERNAME, --username USERNAME
                        web login username
  -p PASSWORD, --password PASSWORD
                        web login password
  -g, --global          global configuration
  -l, --local           local configuration
  -v, --verbosity
  --proxy PROXY         proxy address
  --proxy-username PROXY_USERNAME
                        proxy username
  --proxy-password PROXY_PASSWORD
                        proxy password
  --version             weblinks version
```

## Docs

**Weblinks usage**

To see current lib. version
```shell
weblinks --version
# weblinks version: 2.0
```

To see python file from given url
```shell
weblinks --web https://www.python.org/ftp/python/3.8.13/ --substring Python
# INFO     | 2022-07-23 16:23:33,603 | run     :117  | links found
# Python-3.8.13.tar.xz
# Python-3.8.13.tar.xz.asc
# Python-3.8.13.tgz
# Python-3.8.13.tgz.asc
```

Still wanted to filter add file extention
```shell
weblinks --web https://www.python.org/ftp/python/3.8.13/ --substring Python --ext .tgz
# INFO     | 2022-07-23 16:23:33,603 | run     :117  | links found
# Python-3.8.13.tgz
```

Start download, listed links are good
```shell
weblinks --web https://www.python.org/ftp/python/3.8.13/ --substring Python --ext .tgz -d
# INFO     | 2022-07-23 16:25:34,807 | run     :117  | links found
# Python-3.8.13.tgz
# INFO     | 2022-07-23 16:25:34,807 | run     :124  | start download: Python-3.8.13.tgz
# INFO     | 2022-07-23 16:25:34,807 | utils   :58   | downloading: Python-3.8.13.tgz
# INFO     | 2022-07-23 16:25:36,849 | run     :126  | completed: Python-3.8.13.tgz
```

For authentication
```shell
weblinks --web <url> --substring <sub> --username <kirankotari> --password <xxxxxx> --ext .tgz
# Note: don't add --password, it will ask dynamically
```

For verbose add -v
```shell
weblinks --web <url> --substring <sub> --username <kirankotari> --ext .tgz -v
```

To store config add --local or --global respectively
```shell
weblinks --local --web <url> --username <kirankotari> --ext .tgz
```

For proxy
```shell
weblinks --proxy <ip>:<port> --web <url> --substring <sub>
```

For proxy with authentication
```shell
weblinks --proxy <ip>:<port> --web <url> --substring <sub> --proxy-username <proxy user> --proxy-password <proxy password>
```

Adding web authentication on top of proxy auth.
```shell
weblinks --proxy <ip>:<port> --web <url> --substring <sub> --proxy-username <proxy user> --proxy-password <proxy password> --username <user>
```

## Bug Tracker and Support

- Please report any suggestions, bug reports, or annoyances with weblinks through the [Github bug tracker](https://github.com/kirankotari/weblinks/issues). If you're having problems with general python issues, consider searching for a solution on [Stack Overflow](https://stackoverflow.com/search?q=).
- If you can't find a solution for your problem or need more help, you can [ask a question](https://stackoverflow.com/questions/ask).

## License and Copyright

- weblinks is licensed [Apache 2.0](https://opensource.org/licenses/Apache-2.0) 2022

## Author and Thanks

Weblinks was developed by [Kiran Kumar Kotari](https://github.com/kirankotari)
