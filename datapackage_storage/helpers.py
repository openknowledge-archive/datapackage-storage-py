# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

import os
import re
import six


# Module API

WRITE_MODE = 'w'
if six.PY2:
    WRITE_MODE = 'wb'

WRITE_ENCODING = 'utf-8'
if six.PY2:
    WRITE_ENCODING = None

WRITE_NEWLINE = ''
if six.PY2:
    WRITE_NEWLINE = None


def convert_path(path, name):
    table = os.path.splitext(path)[0]
    table = table.replace(os.path.sep, '__')
    if name is not None:
        table = '___'.join([table, name])
    table = re.sub('[^0-9a-zA-Z_]+', '_', table)
    table = table.lower()
    return table


def restore_path(table):
    name = None
    splited = table.split('___')
    path = splited[0]
    if len(splited) == 2:
        name = splited[1]
    path = path.replace('__', os.path.sep)
    path += '.csv'
    return path, name


def convert_schemas(mapping, schemas):
    for schema in schemas:
        for fk in schema.get('foreignKeys', []):
            resource = fk['reference']['resource']
            if resource != 'self':
                if resource not in mapping:
                    message = (
                        'Resource "%s" for foreign key "%s" '
                        'doesn\'t exist.' % (resource, fk))
                    raise ValueError(message)
                fk['reference']['resource'] = '<table>'
                fk['reference']['table'] = mapping[resource]
    return schemas


def restore_resources(mapping, resources):
    for resource in resources:
        schema = resource['schema']
        for fk in schema.get('foreignKeys', []):
            fkresource = fk['reference']['resource']
            if fkresource == '<table>':
                table = fk['reference']['table']
                _, name = restore_path(table)
                del fk['reference']['table']
                fk['reference']['resource'] = name
    return resources


def ensure_dir(path):
    """Ensure directory exists.

    Parameters
    ----------
    path: str

    """
    dirpath = os.path.dirname(path)
    if dirpath and not os.path.exists(dirpath):
        os.makedirs(dirpath)
