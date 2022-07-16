""" Wanted to fetch the links from web
    and filter them using substring, a file extentions

usage: weblinks.py [-h] [-w WEB] [-u USERNAME] [-p PASSWORD] [-e EXT] [-d]
                   [-v]
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

>>> # print the links from the web
# TODO: need to add how to use the lib.
"""

import logging
import argparse
import validators

from .weblinks import Web
from .utils import get_log
from getpass import getpass


def parser() -> argparse:
    parser = argparse.ArgumentParser()
    parser.add_argument("-w", "--web", required=True, help="the website")
    parser.add_argument("substring", help="the sub-string in the links")
    parser.add_argument("-u", "--username", default=None, help="web login username")
    parser.add_argument("-p", "--password", default=None, help="web login password")
    parser.add_argument("-e", "--ext", default=None, help="file extention")
    parser.add_argument('-d', '--download', action='store_true', help="download links")
    parser.add_argument("-v", "--verbosity", action="count", default=0)
    return parser.parse_args()


def validate_parser(log, args) -> bool:
    if args.web:
        if not validators.url(args.web):
            log.error(f"url `{args.web}` is invalid")
            return False
        if len(args.web.split('/')[-1].split('.')) == 1:
            args.web += '/'
        log.debug(f"given webpage is valid")

    if args.username and not args.password:
        log.debug(f'collecting password for the given username')
        args.password = getpass("enter web password to fetch the links: ")

    return True


def main():
    level=logging.INFO

    args = parser()

    if args.verbosity >= 1:
        level=logging.DEBUG

    log = get_log(level)
    log.debug('initiate args validataion')
    if validate_parser(log, args):
        web = Web(args.web, args.substring, args.ext, level)
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


if __name__ == "__main__":
    main()