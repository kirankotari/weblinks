""" Wanted to fetch the links from web
    and filter them using substring, a file extentions

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
"""

import getpass
import logging
import argparse
import validators

from .proxy import Proxy
from .weblinks import Web
from .utils import get_log
from .config import Configuration


version = "2.0"


def parser() -> argparse:
    parser = argparse.ArgumentParser()
    parser.add_argument("-w", "--web", default=None, help="the website")
    parser.add_argument("-s", "--substring", default=None, help="the sub-string in the links")
    parser.add_argument("-e", "--ext", default=None, help="file extention")
    parser.add_argument('-d', '--download', action='store_true', help="download links")
    parser.add_argument("-u", "--username", default=None, help="web login username")
    parser.add_argument("-p", "--password", default=None, help="web login password")
    parser.add_argument('-g', '--global', action='store_true', help="global configuration")
    parser.add_argument('-l', '--local', action='store_true', help="local configuration")
    parser.add_argument("-v", "--verbosity", action="count", default=0)
    parser.add_argument("--proxy", default=None, help="proxy address")
    parser.add_argument("--proxy-username", default=None, help="proxy username")
    parser.add_argument("--proxy-password", default=None, help="proxy password")
    parser.add_argument("--version", action='store_true', help="weblinks version")
    return parser.parse_args()


def validate_parser(log, args) -> bool:
    if args.web:
        if not validators.url(args.web):
            log.error(f"url `{args.web}` is invalid")
            return False
        if len(args.web.split('/')[-1].split('.')) == 1:
            args.web += '/'
        log.debug(f"given webpage is valid")

    if not args.web:
        log.error(f"-w/--web is mandatory")
        return False

    if not args.substring:
        log.error(f"-s/--substring is mandatory")
        return False

    if args.username and not args.password:
        log.debug(f'collecting password for the given username')
        args.password = getpass.getpass("enter web password to fetch the links: ")

    return True


def main():
    level=logging.INFO

    args = parser()

    if args.__dict__.get('version', None):
        print(f"weblinks version: {version}")
        return

    if args.__dict__.get('verbosity', 0) >= 1:
        level=logging.DEBUG

    log = get_log(level)
    config = Configuration(level)
    proxy = Proxy(level)
    args = config.load(args)

    if args.__dict__.get('global', False):
        config.update_global(args)
        log.debug('configuration stored in global location')
        return

    if args.__dict__.get('local', False):
        config.update_local(args)
        log.debug('configuration stored in local location')
        return

    log.debug('initiate args validataion')
    if validate_parser(log, args):
        args.proxy = proxy.add(args)
        web = Web(args.web, args.substring, args.ext, level, args.proxy)
        log.debug(f'args: {web.hide_password(args.__dict__)}')
        web.setup(args.username, args.password)
        links = web.get_links()
        if not len(links):
            log.warning(f'no links found for {args.substring}')
            return
        log.info('links found')
        for l in links:
            print(l)

        # TODO: need to add status bar..!
        if args.download:
            for l in links:
                log.info(f'start download: {l}')
                web.download(args.web, l)
                log.info(f'completed: {l}')
        return

