#!/usr/bin/env python
# -*- coding: utf-8 -*-

# import threading
import jinja2 as j2
import tornado.template


__all__ = ["JinjaLoader", "JinjaEngine"]


class Base(object):
    mods_recorder = {}

    def __init__(self, *args, **kwargs):
        self.loader = j2.ChoiceLoader([])
        self.top_loader = self.loader.loaders

    @staticmethod
    def create_loader_via_path(searchpath, encoding="utf-8", followlinks=False):
        return j2.FileSystemLoader(searchpath, encoding=encoding, followlinks=followlinks)

    @staticmethod
    def create_loader_via_pkg(package_name, package_path="templates", encoding="utf-8"):
        return j2.PackageLoader(package_name, package_path=package_path, encoding=encoding)

    def register_loader(self, new_loader, mod_name):
        """针对不同的 Loader类型进行过滤重复"""

        is_exist = False
        if isinstance(new_loader, j2.FileSystemLoader):
            exist_file_loader = filter(lambda f: isinstance(f, j2.FileSystemLoader), self.top_loader)
            for loader in exist_file_loader:
                if set(new_loader.searchpath).issubset(set(loader.searchpath)):
                    is_exist = True
                    break

        if not is_exist:
            self.top_loader.append(new_loader)
            self.mods_recorder[mod_name] = new_loader

    def unregister_loader(self, mod_name):
        if self.mods_recorder.get(mod_name):
            if mod_name in self.mods_recorder.keys():
                self.top_loader.remove(self.mods_recorder[mod_name])

            del self.mods_recorder[mod_name]


class TTemplate(object):
    def __init__(self, template_instance):
        self.template_instance = template_instance

    def generate(self, **kwargs):
        return self.template_instance.render(**kwargs)


class JinjaLoader(tornado.template.BaseLoader, Base):
    """
        Bose on tornado.template.BaseLoader.
            *USAGE* child templates uses Base.register_loader to register
                    in tornado.web.RequestHandler function initialize/prepare.
    """

    def __init__(self, root_directory, **kwargs):
        super(JinjaLoader, self).__init__()

        self.loader = j2.ChoiceLoader([])
        self.top_loader = self.loader.loaders

        self.jinja_env = j2.Environment(
            loader=self.loader,
            auto_reload=kwargs.pop("auto_reload", False),
            autoescape=kwargs.pop("autoescape", False),
            **kwargs
        )

        if root_directory:
            self.top_loader.append(j2.FileSystemLoader(root_directory))
            # self.templates = {}
            # self.lock = threading.RLock()

    def resolve_path(self, name, parent_path=None):
        return name

    def _create_template(self, name):
        template_instance = TTemplate(self.jinja_env.get_template(name))
        return template_instance


class JinjaEngine(j2.Environment, Base):
    """
        Bose on jinja2.
            *MUST* override tornado.web.RequestHandler function render.
            *USAGE* child templates use Base.register_loader to register in ModsHandler or
                    register in tornado.web.RequestHandler function initialize/prepare.

        Think:
        一：
            1. 本类创建 self.loader = j2.ChoiceLoader([])
            2. xHandler初始化一个 ctx_template_loader并加入到 self.loader
            3. BaseHandler的 render不用改动，直接search jinja_env

        二:
            1. 本类有一个默认的 self.loader
            2. xHandler初始化一个 self.ctx_template_loader
            3. BaseHandler的 render进行历遍，
    """

    def __init__(self, root_directory=None, loader=None, **kwargs):
        super(JinjaEngine, self).__init__(**kwargs)

        self.loader = j2.ChoiceLoader([])
        self.top_loader = self.loader.loaders

        if loader and isinstance(loader, j2.BaseLoader):
            self.top_loader.append(loader)
        elif root_directory:
            self.top_loader.append(j2.FileSystemLoader(root_directory))

    @property
    def jinja_env(self):
        return self
