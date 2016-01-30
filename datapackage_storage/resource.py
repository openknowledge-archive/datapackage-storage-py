# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

import io
import csv
import json
from tabulator import topen
from jsontableschema.model import SchemaModel

from . import helpers


# Module API

def import_resource(storage, table, schema, data):
    """Import JSONTableSchema resource to storage's table.

    Parameters
    ----------
    storage: object
        Storage object.
    table: str
        Table name.
    schema: str
        Path to schema file.
    data: str
        Path to data file.

    """

    # Create table
    model = SchemaModel(schema)
    schema = model.as_python
    if storage.check(table):
        storage.delete(table)
    storage.create(table, schema)

    # Write data
    with topen(data, with_headers=True) as data:
        storage.write(table, data)


def export_resource(storage, table, schema, data):
    """Export JSONTableSchema resource from storage's table.

    Parameters
    ----------
    storage: object
        Storage object.
    table: str
        Table name.
    schema: str
        Path to schema file.
    data: str
        Path to data file.

    """

    # Save schema
    helpers.ensure_dir(schema)
    with io.open(schema,
                 mode=helpers.WRITE_MODE,
                 encoding=helpers.WRITE_ENCODING) as file:
        schema = storage.describe(table)
        json.dump(schema, file, indent=4)

    # Save data
    helpers.ensure_dir(data)
    with io.open(data,
                 mode=helpers.WRITE_MODE,
                 newline=helpers.WRITE_NEWLINE,
                 encoding=helpers.WRITE_ENCODING) as file:
        model = SchemaModel(schema)
        data = storage.read(table)
        writer = csv.writer(file)
        writer.writerow(model.headers)
        for row in data:
            writer.writerow(row)
