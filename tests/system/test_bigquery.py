# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

import os
import io
import six
import sys
import json
import runpy
import shutil
import tempfile
import unittest


from examples import storages
from examples import bigquery_testing as testing


class TestPackage(unittest.TestCase):

    # Helpers

    def setUp(self):
        self.target = tempfile.mkstemp(dir=tempfile.mkdtemp())[1]

    def tearDown(self):
        try:
            shutil.rmtree(os.path.dirname(self.target))
        except Exception:
            pass

    # Tests

    def test_testing(self):

        # Run function
        storages.bigquery.run(testing.dataset, testing.prefix, testing.source, self.target, 'testing')

        # Assert schemas
        source = json.load(io.open(testing.source, encoding='utf-8'))
        target = json.load(io.open(self.target, encoding='utf-8'))
        assert source == target

        # Assert data
        for source, target in zip(source['resources'], target['resources']):
            spath = os.path.join(os.path.dirname(testing.source), source['path'])
            tpath = os.path.join(os.path.dirname(self.target), target['path'])
            source = io.open(spath, encoding='utf-8').read()
            target = io.open(tpath, encoding='utf-8').read()
            assert source == target
