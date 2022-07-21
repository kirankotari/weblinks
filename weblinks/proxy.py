from __future__ import absolute_import

import json
from pathlib import Path
from logging import INFO
from .utils import Utils


class Proxy(Utils):
    def __init__(self, level=INFO) -> None:
        super().__init__(level)

    # curl -x http://<user>:<pass>@<proxyhost>:<port>/
    #  -o <filename> -L <link>
    def add(self, args):
        if not args.proxy_username:
            self.log.debug('adding proxy data')
            return args.proxy

        if '//' in args.proxy and args.proxy_username:
            p = str(args.proxy).split('//')
            self.log.debug('adding proxy data with username and password')
            proxy = f"{p[0]}//{args.proxy_username}:{args.proxy_password}@{p[-1]}"
            return proxy
        
        if args.proxy_username:
            self.log.debug('adding proxy data with username and password')
            proxy = f"{args.proxy_username}:{args.proxy_password}@{args.proxy}"
            return proxy
