# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

import sys
from sqlalchemy import create_engine

import jtssql
import datapackage_storage


def run(url, prefix, source, target, datapackage_name):

    # Storage
    engine = create_engine(url)
    storage = jtssql.Storage(engine=engine, prefix=prefix)

    # Import package
    datapackage_storage.import_package(storage, source)
    print('Imported datapackage from "%s"' % source)

    # Export package
    datapackage_storage.export_package(storage, target, datapackage_name)
    print('Exported datapackage to "%s"' % target)
