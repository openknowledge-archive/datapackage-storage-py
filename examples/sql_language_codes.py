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
url = 'sqlite:///:memory:'
prefix = 'language_codes_%s_%s_' % (sys.version_info.major, sys.version_info.minor)
source = 'examples/packages/language-codes/datapackage.json'
target = 'tmp/sql/packages/language-codes/datapackage.json'


# Execution
if __name__ == '__main__':
    storages.sql.run(url, prefix, source, target, 'package')
