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
import sys
import string
import logging
import subprocess
import validators

from getpass import getpass
from pathlib import Path

# TODO: simple way of collecting links from html page
# TODO: running os commands like curl

class System:
    cmd = ["curl", "-k"]

    def __init__(self, log):
        self.log = log

    def update_command(self, args):
        if args.username:
            self.cmd += ["-u", f"{args.username}:{args.password}"]

    def download(self, web, list_files):
        for each in list_files:
            self.log.info(f"downloading: {each}")
            self.run([f"{web}{each}", "-o", f"{each}"])

    def run(self, cmd):
        subprocess.call(self.cmd + cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True

class Web(System):
    def __init__(self, name, log) -> None:
        super().__init__(log)
        self.name = name

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

class Args:
    @staticmethod
    def get_parser():
        parser = argparse.ArgumentParser(
            prog='weblinks',
            add_help=False
        )
        parser.add_argument("substring", help="sub-string filter")
        parser.add_argument("-w", "--web", default=None, help="the website")
        parser.add_argument("-u", "--username", default=None, help="web login username")
        parser.add_argument("-p", "--password", default=None, help="web login password")
        parser.add_argument("-e", "--ext", default=None, help="file extention")
        parser.add_argument('-d', '--download', action='store_true', help="download links")
        parser.add_argument("-v", "--verbosity", action="count", default=0)

        parent_config_parser = argparse.ArgumentParser(
            prog='weblinks',
            add_help=False
        )
        parent_config_parser.add_argument('-w', '--web', nargs="?", default=None, help='web site url')
        parent_config_parser.add_argument('-u', '--username', nargs="?", default=None, help='web site username')
        parent_config_parser.add_argument("-e", "--ext", nargs="?", default=None, help="file extention")
        parent_config_parser.add_argument('-d', '--download', action='store_true', help="download links")
        parent_config_parser.add_argument('-s', '--show', default=False, action='store_true', help="display configuration")

        config_main_parser = argparse.ArgumentParser(
            prog='weblinks'
        )
        config_parsers = config_main_parser.add_subparsers(title="configuration", dest="config")
        config_parsers.add_parser("substring", help="the sub-string in the links", parents=[parser])
        config_parsers.add_parser("local", help="weblinks local configuration", parents=[parent_config_parser])
        config_parsers.add_parser("global", help="weblinks global configuration", parents=[parent_config_parser])
        return config_main_parser.parse_args()

    @staticmethod
    def validate(args, obj):
        if args.web:
            if not validators.url(args.web):
                obj.log.error(f"Given url `{args.web}` is invalid")
                exit(-1)
            if len(args.web.split('/')[-1].split('.')) == 1:
                args.web += '/'

        if args.username and not args.password:
            args.password = getpass("enter web password to fetch the links: ")
        return args

    @staticmethod
    def hide(dict):
        temp = dict.copy()
        temp['password'] = 'xxxxxxx'
        return temp


class CustomLogger:
    @staticmethod
    def add_trace():
        def _trace(logger, message, *args, **kwargs):
            if logger.isEnabledFor(logging.TRACE):
                logger._log(logging.TRACE, message, args, **kwargs)

        def __create_trace_log_level():
            "Add TRACE log level and Logger.trace() method."

            logging.TRACE = 5
            logging.addLevelName(logging.TRACE, "TRACE")

            logging.Logger.trace = _trace
            return logging
        return __create_trace_log_level()

    @staticmethod
    def set_log(logging, log_level, name):
        format = '%(levelname)s | %(name)s | %(message)s'
        logging.basicConfig(
            stream=sys.stdout, 
            level=log_level, 
            format=format, 
            datefmt=None
        )
        logger = logging.getLogger(name)
        logger.setLevel(log_level)
        return logger


def main():
    name = "Weblinks"
    args = Args.get_parser()
    logging = CustomLogger.add_trace()
    log_level = None
    if args.verbosity >= 2: 
        log_level = logging.TRACE
    elif args.verbosity >= 1:
        log_level = logging.DEBUG
    else:
        log_level = logging.INFO
    log = CustomLogger.set_log(logging, log_level, name)

    obj = Web(name, log)
    log.trace(f"Running '{__file__}'")
    log.debug(f"Given arguments {Args.hide(args.__dict__)}")

    args = Args.validate(args, obj)

    def links():
        obj.update_command(args)
        return obj.get_links()

    urls = links()
    if not len(urls):
        log.info(f"No links found in {args.web}")
        exit(-1)

    log.info("links found:")
    log.info("============")
    for each in links():
        log.info(each)

    if args.download:
        log.info("============")
        obj.download(args.web, links)


if __name__ == "__main__":
    main()