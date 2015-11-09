import os
import stristo
import unittest
import tempfile
import re
import ast


class StristoReadWriteTest(unittest.TestCase):

    def setUp(self):
        stristo.app.testing = True  # Enable debug message forwarding
        self.app = stristo.app.test_client()

    def tearDown(self):
        pass

    def test_receive_token(self):
        resp = self.app.get('/write/Hello')
        print "Response :: %s" % resp.data
        token_reg = re.compile("[a-z0-9]+")
        assert token_reg.match(resp.data)

    def test_write_to_token(self):
        resp_0 = self.app.get('/write/FirstString')
        print "Response :: %s" % resp_0.data
        token_0 = resp_0.data

        resp_1 = self.app.get('/write/%s/SecondString' % token_0)
        print "Response :: %s" % resp_1.data
        token_1 = resp_1.data

        assert token_0 == token_1

    def test_read_single(self):
        resp_write = self.app.get('/write/ThisIsATestString')
        resp_read = self.app.get('/read/%s' % resp_write.data)
        print "Response :: %s" % ast.literal_eval(resp_read.data)[0]
        assert ast.literal_eval(resp_read.data)[0] == 'ThisIsATestString'

    def test_read_multiple(self):
        resp_write_0 = self.app.get('/write/FirstString')
        token = resp_write_0.data
        self.app.get('/write/%s/SecondString' % token)

        resp_read = self.app.get('/read/%s/2' % token)
        print "Response :: %s" % ast.literal_eval(resp_read.data)

        assert ast.literal_eval(resp_read.data)[0] == 'SecondString'
        assert ast.literal_eval(resp_read.data)[1] == 'FirstString'

    def test_read_single_full(self):
        resp_write = self.app.get('/write/ThisIsAnotherTestString')
        resp_read = self.app.get('/readfull/%s/1' % resp_write.data)
        print "Response :: %s" % ast.literal_eval(resp_read.data)

        expected = [{'value': 'ThisIsAnotherTestString',
                    'created': '2015-11-06 11:16:00.679551'}]

        date_reg = re.compile("\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}.\d{6}$")

        assert ast.literal_eval(resp_read.data)[0]['value'] == \
            'ThisIsAnotherTestString'
        assert date_reg.match(ast.literal_eval(resp_read.data)[0]['created'])

    def test_read_single_invalid_token(self):
        resp_read = self.app.get('/read/THIS_IS_AN_INVALID_TOKEN')
        print "Response :: %s" % resp_read.status_code
        assert resp_read.status_code == 400
        assert ast.literal_eval(resp_read.data)['status'] == "ERROR"

    def test_read_single_full_invalid_token(self):
        resp_read = self.app.get('/readfull/THIS_IS_AN_INVALID_TOKEN/10')
        print "Response :: %s" % resp_read.status_code
        assert resp_read.status_code == 400
        assert ast.literal_eval(resp_read.data)['status'] == "ERROR"

    def test_write_invalid_token(self):
        resp_write = self.app.get('/write/THIS_IS_AN_INVALID_TOKEN/MessageHere')
        print "Response :: %s" % resp_write.status_code
        assert resp_write.status_code == 400
        assert ast.literal_eval(resp_write.data)['status'] == "ERROR"


if __name__ == '__main__':
    unittest.main()
