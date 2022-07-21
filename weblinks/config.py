from __future__ import absolute_import

import json
from pathlib import Path
from logging import INFO
from .utils import Utils


class Configuration(Utils):
    def __init__(self, level=INFO) -> None:
        super().__init__(level)
        self.path = '.weblinks'
        self.local_path = Path(f'./{self.path}').expanduser().absolute()
        self.global_path = Path(f'~/{self.path}').expanduser().absolute()

    def read_json(self, path):
        with open(path, 'r') as f:
            data = json.load(f)
        return data

    def update_not_none(self, data, args):
        for k, v in args.items():
            if not v and k in data:
                continue
            data[k] = args[k]
        return data

    def load(self, args):
        data = {}
        if self.local_path.exists():
            data = self.read_json(self.local_path)
        if self.global_path.exists():
            data = self.read_json(self.global_path)
        args.__dict__ = self.update_not_none(data, args.__dict__)
        self.log.debug(self.hide_password(args.__dict__))
        self.log.debug(f'configuration loaded')
        return args

    def update_global(self, args):
        self.global_path.touch(exist_ok=True)
        self.log.debug(f'path: {self.global_path}')
        with open(self.global_path, 'w') as f:
            del args.__dict__['global']
            json.dump(args.__dict__, f)
        return

    def update_local(self, args):
        self.local_path.touch(exist_ok=True)
        self.log.debug(f'path: {self.local_path}')
        with open(self.local_path, 'w') as f:
            del args.__dict__['local']
            json.dump(args.__dict__, f)
        return

