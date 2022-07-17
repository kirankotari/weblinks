"""
The module is for system operations (subprocess) and setting logger
"""

import random
import string
import logging
import subprocess


format = '%(levelname)-8s | %(asctime)s | %(module)-8s:%(lineno)-4d | %(message)s'

def get_log(level):
    logging.basicConfig(level=level, format=format)
    return logging.getLogger()


class Utils:
    def __init__(self, level=logging.INFO) -> None:
        super(Utils, self).__init__()
        self.log = get_log(level)
        self.log.debug(f"base class: {__class__.__name__} initialize")

    def get_name(self) -> str:
        name = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))
        self.log.debug(f'random name: {name}')
        return name

    def read(self, fpath) -> str:
        with open(fpath, 'r') as f:
            self.log.debug(f'reading file from {fpath}')
            return f.read()

    def hide_password(self, dict) -> dict:
        temp = dict.copy()
        temp['password'] = 'xxxxxxx'
        self.log.debug(f'password masked')
        return temp


class System:
    """
    In this class we are running curl commands to fetch the web data.
    """
    cmd = ["curl", "-k"]

    def __init__(self, level=logging.INFO) -> None:
        super(System, self).__init__()
        self.log = get_log(level)
        self.log.debug(f"base class: {__class__.__name__} initialize")

    def setup(self, username=None, password=None) -> None:
        if username:
            self.cmd += ["-u", f"{username}:{password}"]
            self.log.debug(f"adding user details to the command")

    def download(self, web, fname) -> None:
        self.log.info(f"downloading: {fname}")
        # "--progress-bar" which is supressed by subprocess.call
        self.run([f"{web}{fname}", "-o", f"{fname}"])

    def run(self, cmd) -> bool:
        self.log.debug(f"executing curl command: {' '.join(self.cmd + cmd)}")
        res = subprocess.call(self.cmd + cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if res:
            self.log.error(f"command: `{' '.join(cmd)}`, check reachability")
            return False
        return True