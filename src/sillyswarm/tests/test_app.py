# -*- coding: utf-8 -*-
#
# Copyright 2011 Tobias Rodäbel
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Unit tests for the Silly Swarm server-side code."""

import os
import unittest


class test_handlers(unittest.TestCase):
    """Testing webapp handlers."""

    def setUp(self):
        """Set up test environment."""

        from google.appengine.api import apiproxy_stub_map
        from google.appengine.api.memcache import memcache_stub
        from typhoonae.websocket import websocket_stub

        os.environ['APPLICATION_ID'] = "test"
        os.environ['AUTH_DOMAIN'] = "example.com"
        os.environ['SERVER_NAME'] = "test"

        if not apiproxy_stub_map.apiproxy.GetStub('memcache'):
            # Initialize Memcache Service
            memcache = memcache_stub.MemcacheServiceStub()
            apiproxy_stub_map.apiproxy.RegisterStub('memcache', memcache)

        if not apiproxy_stub_map.apiproxy.GetStub('websocket'):
            # Initialize Web Socket Service
            websocket = websocket_stub.WebSocketServiceStub('localhost')
            apiproxy_stub_map.apiproxy.RegisterStub('websocket', websocket)

    def test_index(self):
        """Browsing the index page."""

        from sillyswarm import app
        from webtest import AppError, TestApp

        app = TestApp(app.app)

        res = app.get('/')
