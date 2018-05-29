# coding: utf-8

import json
from decimal import Decimal
from tornado.httputil import url_concat
from base.tests.helpers.testing import TestBase
from base.application.lookup import responses


class TestShortener(TestBase):

    def test_put_and_get_something_not_exists(self):

        res = self.fetch('/api/short',  method='PUT', body=json.dumps({
            'url': 'http://google.com'
        }))

        res = self.fetch('/api/short/xxx')
        self.assertEqual(res.code, 400)



    def test_put_and_get_putted(self):

        res = self.fetch('/api/short',  method='PUT', body=json.dumps({
            'url': 'http://google.com'
        }))
        jres = json.loads(res.body.decode('utf-8'))

        self.assertEqual(res.code, 200)
        self.assertTrue('id' in jres)

        _id = jres['id']

        res = self.fetch('/api/short/{}'.format(_id))

        self.assertEqual(res.code, 200)
        jres = json.loads(res.body.decode('utf-8'))
        self.assertEqual(jres['url'], 'http://google.com')



