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

from getpass import getpass
from pathlib import Path

# TODO: simple way of collecting links from html page
# TODO: running os commands like curl

class System:
    cmd = ["curl", "-k"]

    def setup(self, args):
        if args.username:
            self.cmd += ["-u", f"{args.username}:{args.password}"]

    def download(self, web, list_files):
        for each in list_files:
            print(f"downloading: {each}")
            self.run([f"{web}{each}", "-o", f"{each}"])

    def run(self, cmd):
        subprocess.call(self.cmd + cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True

class Web(System):
    def __init__(self) -> None:
        self.log = self.get_logger()
        self.args = self.get_parser()

    def get_logger(self):
        pass

    def get_links(self):
        html = self.get_webpage()
        if self.args.ext:
            files = re.findall(f'href="(.*?{self.args.substring}.*\.{self.args.ext})"', html)
        else:
            files = re.findall(f'href="(.*?{self.args.substring}.*)"', html)
        return files

    def get_name(self):
        return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))

    def read(self, fpath):
        with open(fpath, 'r') as f:
            return f.read()

    def get_webpage(self):
        name = self.get_name()
        if self.run([f"{self.args.web}", f"-o", f"{name}.html"]):
            html = self.read(f"{name}.html")
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
    if args.verbosity >= 2:
        # TODO: need to update to obj.log.info("")
        print(f"Running '{__file__}'")
    if args.verbosity >= 1:
        print(f"Given arguments {obj.hide_password(args.__dict__)}")

    if args.web:
        if not validators.url(args.web):
            print(f"Given url `{args.web}` is invalid")
            exit(-1)
        if len(args.web.split('/')[-1].split('.')) == 1:
            args.web += '/'

    if args.username and not args.password:
        args.password = getpass("enter web password to fetch the links: ")

    obj.setup(args)
    links = obj.get_links()
    print("links found:")
    print("============")
    for each in links:
        print(each)
    if args.download:
        print("============")
        obj.download(args.web, links)


if __name__ == "__main__":
    main()