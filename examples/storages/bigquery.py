# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

import io
import os
import sys
import json
from apiclient.discovery import build
from oauth2client.client import GoogleCredentials

import jtsbq
import datapackage_storage


def run(dataset, prefix, source, target, datapackage_name):

    # Storage
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '.credentials.json'
    credentials = GoogleCredentials.get_application_default()
    service = build('bigquery', 'v2', credentials=credentials)
    project = json.load(io.open('.credentials.json', encoding='utf-8'))['project_id']
    storage = jtsbq.Storage(service, project, dataset, prefix=prefix)

    # Import package
    datapackage_storage.import_package(storage, source)
    print('Imported datapackage from "%s"' % source)

    # Export package
    datapackage_storage.export_package(storage, target, datapackage_name)
    print('Exported datapackage to "%s"' % target)
