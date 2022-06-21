""" Goal: Wanted to fetch the links from web
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
import argparse
import random
import re
import os
import string
import subprocess
import validators
import logging

from getpass import getpass
from pathlib import Path

format = '%(levelname)-8s | %(asctime)s | %(module)s:%(lineno)-4d | %(message)s'


def get_log(level):
    logging.basicConfig(level=level, format=format)
    return logging.getLogger()


class System:
    cmd = ["curl", "-k"]
    log = get_log(logging.INFO)

    def setup(self, args):
        if args.username:
            self.cmd += ["-u", f"{args.username}:{args.password}"]

    def download(self, web, list_files):
        for each in list_files:
            self.log.info(f"downloading: {each}")
            self.run([f"{web}{each}", "-o", f"{each}"])

    def run(self, cmd):
        res = subprocess.call(self.cmd + cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if res:
            self.log.error(f"command: `{' '.join(cmd)}`, check reachability")
            return False
        return True

class Web(System):
    def __init__(self) -> None:
        self.args = self.get_parser()

    def get_links(self):
        html = self.get_webpage(delete_copy=True)
        if html is None:
            self.log.error("Couldn't able to read html page")
            return
        if self.args.ext:
            files = re.findall(f'href\=\"(.*{self.args.substring}.*.{self.args.ext})\"', html)
        else:
            files = re.findall(f'href\=\"(.*?{self.args.substring}.*)\"', html)
        return files

    def get_name(self):
        return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))

    def read(self, fpath):
        with open(fpath, 'r') as f:
            return f.read()

    def get_webpage(self, delete_copy=True):
        name = self.get_name()
        if self.run([f"{self.args.web}", f"-o", f"./{name}.html"]):
            html = self.read(f"{name}.html")
            if delete_copy:
                self.log.debug(f"removing temporary files, {name}.html")
                os.unlink(f"{name}.html")
            return html

    def hide_password(self, dict):
        temp = dict.copy()
        temp['password'] = 'xxxxxxx'
        return temp

    def get_parser(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("-w", "--web", required=True, help="the website")
        parser.add_argument("substring", help="the sub-string in the links")
        parser.add_argument("-u", "--username", default=None, help="web login username")
        parser.add_argument("-p", "--password", default=None, help="web login password")
        parser.add_argument("-e", "--ext", default=None, help="file extention")
        parser.add_argument('-d', '--download', action='store_true', help="download links")
        parser.add_argument("-v", "--verbosity", action="count", default=0)
        return parser.parse_args()


def main():
    obj = Web()
    args = obj.args
    level=logging.INFO
    if args.verbosity >= 1:
        level=logging.DEBUG
    
    obj.log = get_log(level)
    obj.log.debug(f"Running '{__file__}'")
    obj.log.debug(f'args: {obj.hide_password(args.__dict__)}')

    if args.web:
        if not validators.url(args.web):
            obj.log.error(f"url `{args.web}` is invalid")
            exit(-1)
        if len(args.web.split('/')[-1].split('.')) == 1:
            args.web += '/'

    if args.username and not args.password:
        args.password = getpass("enter web password to fetch the links: ")

    obj.setup(args)
    links = obj.get_links()
    if links is None:
        exit(-1)

    if not len(links):
        obj.log.warning(f"no links found in {args.web}")
        exit(-1)

    obj.log.info("links found:")
    for each in links:
        print(each)

    if args.download:
        obj.log.info("started downloading files")
        print("============")
        obj.download(args.web, links)
        obj.log.info("downloading completed.")


if __name__ == "__main__":
    main()