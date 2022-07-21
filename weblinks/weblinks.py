from __future__ import absolute_import

import re
import os

from logging import INFO
from typing import Union
from .utils import System, Utils


class Web(Utils, System):
    def __init__(self, web, substring, ext=None, level=INFO, proxy=None) -> None:
        super(Web, self).__init__(level)
        self.log.debug(f"class: {__class__.__name__} initialize")
        self.ext = ext
        self.web = web
        self.proxy = proxy
        self.filter = substring

    def get_links(self) -> list:
        self.log.debug(f"fetch weblinks")
        html = self.get_webpage(delete_copy=True)
        if html is None:
            self.log.error("couldn't able to read html page")
            return []
        self.log.debug(f"applying filters")
        if self.ext:
            files = re.findall(fr'href="(.*{self.filter}.*.{self.ext})"', html)
        else:
            files = re.findall(fr'href="(.*?{self.filter}.*)"', html)
        self.log.debug(f'found: {len(files)} files')
        return files

    def get_webpage(self, delete_copy=True) -> Union[str, None]:
        name = self.get_name()
        self.log.debug(f"download webpage: {name}.html")
        params = []
        if self.proxy:
            params = ['-x', self.proxy]
        params += [f"{self.web}", f"-o", f"./{name}.html"]
        if self.run(params):
            html = self.read(f"{name}.html")
            self.log.debug(f"read webpage: {name}.html")
            if delete_copy:
                self.log.debug(f"delete webpage: {name}.html")
                os.unlink(f"{name}.html")
            return html
