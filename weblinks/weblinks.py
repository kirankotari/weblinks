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
import pickle
import string
import logging
import subprocess
import validators

from getpass import getpass
from pathlib import Path


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

    def exist(self, path):
        p = Path(path).expanduser().absolute()
        return p.exists()

    def pickle_read(self, path):
        p = Path(path).expanduser().absolute().as_posix()
        with open(p, 'rb') as f:
            return pickle.load(f)

    def pickle_write(self, path, data):
        p = Path(path).expanduser().absolute().as_posix()
        with open(p, 'wb') as f:
            pickle.dump(data, f)

class Web(System):
    def __init__(self, name, log, args) -> None:
        super().__init__(log)
        self.name = name
        self.args = args
        self.global_path = '~/.weblinks'
        self.local_path = './.weblinks'

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
        if not self.args.web:
            self.log.error(f'web link is missing got: `{self.args.web}`')
            exit(-1)
        name = self.get_name()
        if self.run([f"{self.args.web}", f"-o", f"{name}.html"]):
            html = self.read(f"{name}.html")
            os.unlink(f"{name}.html")
            return html

    def fetch_config(self, path):
        if self.exist(path):
            return self.pickle_read(path)
        return False

    def config(self, path):
        if self.args.show:
            data = self.fetch_config(path)
            msg = "No configuration found."
            self.log.info(data) if data else self.log.error(msg)
            return

        d = dict()
        if self.args.web is not None:
            d['web'] = self.args.web
        if self.args.username is not None:
            d['username'] = self.args.username
        if self.args.ext is not None:
            d['ext'] = self.args.ext
        if self.args.download is not None:
            d['download'] = self.args.download
        self.__update_config(path, d)

    def __update_config(self, path, data):
        if not self.exist(path):
            self.pickle_write(path, data)
            return
        d = self.pickle_read(path)
        d.update(data)
        self.pickle_write(path, d)

    def update_args(self, d):
        if not self.args.web:
            self.args.web = d.get('web')
        if not self.args.username:
            self.args.username = d.get('username')
        if not self.args.ext:
            self.args.ext = d.get('ext')
        if not self.args.download:
            self.args.download = d.get('download')
        return self.args


class Args:
    @staticmethod
    def get_parser(args=None):
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
        parent_config_parser.add_argument('--no-download', action='store_false', help="do not download links")
        parent_config_parser.add_argument('-s', '--show', action='store_true', help="display configuration")
        parent_config_parser.add_argument("-v", "--verbosity", action="count", default=0)

        config_main_parser = argparse.ArgumentParser(
            prog='weblinks'
        )
        config_parsers = config_main_parser.add_subparsers(title="configuration", dest="config")
        config_parsers.add_parser("substring", help="the sub-string in the links", parents=[parser])
        config_parsers.add_parser("local", help="weblinks local configuration", parents=[parent_config_parser])
        config_parsers.add_parser("global", help="weblinks global configuration", parents=[parent_config_parser])
        return config_main_parser.parse_args(args)

    @staticmethod
    def validate(args, log):
        if args.web:
            if not validators.url(args.web):
                log.error(f"Given url `{args.web}` is invalid")
                exit(-1)
            if len(args.web.split('/')[-1].split('.')) == 1:
                args.web += '/'

        if args.config != 'substring':
            return args

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

    args = Args.validate(args, log)
    obj = Web(name, log, args)
    log.trace(f"Running '{__file__}'")
    log.debug(f"Given arguments {Args.hide(args.__dict__)}")

    if args.config == 'global':
        obj.config(obj.global_path)
        return
    elif args.config == 'local':
        obj.config(obj.local_path)
        return

    # fetch config
    d = obj.fetch_config(obj.local_path)
    if not d:
        d = obj.fetch_config(obj.global_path)

    if d:
        obj.update_args(d)
    def links():
        obj.update_command(obj.args)
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