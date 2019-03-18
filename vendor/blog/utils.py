#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib.parse

from six.moves import urllib_parse as urllib

from vendor.blog.model import Blog


def tp_get_post_tags(db, post_id):
    query_result = db.query(Blog).get(post_id)
    return ((tag.tag_key, tag.tag_value) for tag in query_result.tags)


def view_get_all_tags(db):
    query_tag = db.query(Blog) \
        .filter(Blog.type == Blog.eMeta.type_of_tag)
    tags = [(tag.alias, tag.title) for tag in query_tag]
    return tags


def html_compile(content):
    split_space = lambda string, char=" ": filter(lambda t: t.rstrip(), string.split(char))
    split_space2 = lambda string, char=" ": string.rstrip().split(char)

    output = []
    lines = split_space2(content, char="\n")
    for line in lines:
        _ = line.strip()
        if all([_.startswith("<"), _.endswith(">")]):
            output.append(_)
        else:
            output.append("<p>" + line + "</p>")

    return "\n".join(output)


def setup_page(query_arguments, posts_count, page_flag="page", batch_length=2, batch_size=10):
    def rtn_none(size):
        return [None] * size

    def rtn_data(data):
        return "?" + urllib.urlencode(data, doseq=True)

    max_pg = int((posts_count + batch_size - 1) / batch_size)

    current_pg = 1
    if page_flag in query_arguments:
        current_pg = int(query_arguments[page_flag][0])
    if current_pg < 1:
        current_pg = 1
    elif current_pg > max_pg:
        current_pg = max_pg

    offset = batch_length + 1
    l_differ = current_pg - offset
    r_differ = max_pg - (current_pg + offset)
    if l_differ <= 0:
        _lower_pg = current_pg + 1 - batch_length
        _lower_pg = _lower_pg <= 0 and 1 or _lower_pg

    # elif r_differ <= 0:
    else:
        _lower_pg = current_pg + 1 - batch_length

    pg_items = [_ for _ in range(_lower_pg, _lower_pg + batch_length + 1)]

    if current_pg == 1 or current_pg == max_pg:
        pg_items.pop(-1)
    else:
        pg_items.remove(current_pg)

    batch = [(i, rtn_data({**query_arguments, **{page_flag: i}})) for i in pg_items]

    return current_pg, iter(batch)
