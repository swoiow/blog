#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from configparser import ConfigParser


class ModConfig(object):

    def __init__(self, path):
        self.cfg = ConfigParser()
        self.cfg_path = path

        self.read()

    def read(self):
        if os.path.exists(self.cfg_path):
            self.cfg.read(self.cfg_path)

        else:
            self.cfg["MODULE"] = {}
            self.cfg["MODULE"]["total"] = "lib.cores.mods"
            self.cfg["MODULE"]["enable"] = "lib.cores.mods"

            with open(self.cfg_path, "w") as configfile:
                self.cfg.write(configfile)

    def get_value_by_col_key(self, col, key):
        result = self.cfg.get(col, key).strip().split("\n")
        result = [r for r in result if r]

        return result
