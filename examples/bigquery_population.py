# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

import sys
from pprint import pprint

sys.path.insert(0, '.')
from examples import storages


# Fixtures
dataset = 'datapackage'
prefix = 'population_%s_%s_' % (sys.version_info.major, sys.version_info.minor)
source = 'examples/packages/population/datapackage.json'
target = 'tmp/packages/population/datapackage.json'


# Execution
if __name__ == '__main__':
    storages.bigquery.run(dataset, prefix, source, target, 'package')
