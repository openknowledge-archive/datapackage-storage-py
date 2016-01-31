# datapackage-storage-py

[![Travis](https://img.shields.io/travis/okfn/datapackage-storage-py.svg)](https://travis-ci.org/okfn/datapackage-storage-py)
[![Coveralls](http://img.shields.io/coveralls/okfn/datapackage-storage-py.svg?branch=master)](https://coveralls.io/r/okfn/datapackage-storage-py?branch=master)

A Python library for storing Data Packages in different storages.

## Import/Export

> See section below how to get tabular storage object.

High-level API is easy to use.

Having Data Package in current directory we can import it to storage:

```python
import datapackage_storage

datapackage_storage.import_package(<storage>, 'descriptor.json')
```

Also we can export it from storage:

```python
import datapackage_storage

datapackage_storage.export_package(<storage>, 'descriptor.json', 'datapackage_name')
```

## Tabular Storage

On level between the high-level interface and low-level driver
package uses **Tabular Storage** concept:

![Tabular Storage](diagram.png)

### BigQuery

Install `jsontableschema-bigquery-py` package.

To start using Google BigQuery service:
- Create a new project - [link](https://console.developers.google.com/home/dashboard)
- Create a service key - [link](https://console.developers.google.com/apis/credentials)
- Download json credentials and set `GOOGLE_APPLICATION_CREDENTIALS` environment variable

We can get storage this way:

```python
import io
import os
import json
import jtsbq
from apiclient.discovery import build
from oauth2client.client import GoogleCredentials

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '.credentials.json'
credentials = GoogleCredentials.get_application_default()
service = build('bigquery', 'v2', credentials=credentials)
project = json.load(io.open('.credentials.json', encoding='utf-8'))['project_id']
storage = jtsbq.Storage(service, project, 'dataset', prefix='prefix')
```

### SQL

Install `jsontableschema-sql-py` package.

SQLAlchemy is used as sql wrapper. We can get storage this way:

```python
import jtssql
from sqlalchemy import create_engine

engine = create_engine('sqlite:///:memory:', prefix='prefix')
storage = jtssql.Storage(engine)
```

## Mappings

```
datapackage.json -> *not stored*
datapackage.json resources -> storage tables
data/data.csv schema -> storage table schema
data/data.csv data -> storage table data
```
