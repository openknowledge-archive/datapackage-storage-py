# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

import io
import os
import csv
import json
from copy import deepcopy
from jsontableschema.model import SchemaModel
from datapackage import DataPackage

from . import helpers


# Module API

def import_package(storage, descriptor):
    """Import Data Package to storage.

    Parameters
    ----------
    storage: object
        Storage object.
    descriptor: str
        Path to descriptor.

    """

    # Init maps
    tables = []
    schemas = []
    datamap = {}
    mapping = {}

    # Init model
    model = DataPackage(descriptor)

    # Collect tables/schemas/data
    for resource in model.resources:
        name = resource.metadata.get('name', None)
        table = helpers.convert_path(resource.metadata['path'], name)
        schema = resource.metadata['schema']
        data = resource.iter()
        tables.append(table)
        schemas.append(schema)
        datamap[table] = data
        if name is not None:
            mapping[name] = table
    schemas = helpers.convert_schemas(mapping, schemas)

    # Create tables
    for table in tables:
        if storage.check(table):
            storage.delete(table)
    storage.create(tables, schemas)

    # Write data to tables
    for table in storage.tables:
        if table in datamap:
            storage.write(table, datamap[table])


def export_package(storage, descriptor, datapackage_name):
    """Export Data Package from storage.

    Parameters
    ----------
    storage: object
        Storage object.
    descriptor: str
        Path where to store descriptor.
    datapackage_name: str
        Name of the exported datapackage.

    """

    # Iterate over tables
    resources = []
    mapping = {}
    for table in storage.tables:

        # Prepare
        schema = storage.describe(table)
        base = os.path.dirname(descriptor)
        path, name = helpers.restore_path(table)
        fullpath = os.path.join(base, path)
        if name is not None:
            mapping[table] = name

        # Write data
        helpers.ensure_dir(fullpath)
        with io.open(fullpath,
                     mode=helpers.WRITE_MODE,
                     newline=helpers.WRITE_NEWLINE,
                     encoding=helpers.WRITE_ENCODING) as file:
            model = SchemaModel(deepcopy(schema))
            data = storage.read(table)
            writer = csv.writer(file)
            writer.writerow(model.headers)
            for row in data:
                writer.writerow(row)

        # Add resource
        resource = {'schema': schema, 'path': path}
        if name is not None:
            resource['name'] = name
        resources.append(resource)

    # Write descriptor
    resources = helpers.restore_resources(mapping, resources)
    helpers.ensure_dir(descriptor)
    with io.open(descriptor,
                 mode=helpers.WRITE_MODE,
                 encoding=helpers.WRITE_ENCODING) as file:
        descriptor = {
            'name': datapackage_name,
            'resources': resources,
        }
        json.dump(descriptor, file, indent=4)
