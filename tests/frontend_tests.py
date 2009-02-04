#!/usr/bin/env python

import os
import unittest
from webtest import TestApp, AppError

from google.appengine.api import apiproxy_stub_map, user_service_stub, datastore_file_stub

from backend import application

class BooksTest(unittest.TestCase):

    def setUp(self):
        self.app = TestApp(application)
        os.environ['APPLICATION_ID'] = "temp"
        os.environ['USER_EMAIL'] = "test@example.com"
        os.environ['SERVER_NAME'] = "localhost"
        os.environ['SERVER_PORT'] = "8080"
        
        apiproxy_stub_map.apiproxy = apiproxy_stub_map.APIProxyStubMap()
        apiproxy_stub_map.apiproxy.RegisterStub('user', user_service_stub.UserServiceStub())
        stub = datastore_file_stub.DatastoreFileStub('temp', '/dev/null', '/dev/null')
        apiproxy_stub_map.apiproxy.RegisterStub('datastore_v3', stub)

    def test_thumbnail_renders(self):
        # post image binary
        # request url based on key
        # check image/png header
        # check status code
        pass
        
    def test_image_renders(self):
        # post image binary
        # request url based on key
        # check image/png header
        # check status code
        pass