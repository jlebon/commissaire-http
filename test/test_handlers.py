# Copyright (C) 2016  Red Hat, Inc
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
Test for commissaire_http.handlers module.
"""

from . import TestCase
from commissaire_http import handlers

UID = '123'


class Test_create_response(TestCase):
    """
    Test for the create_response helper function.
    """

    def test_create_response_without_result_or_error(self):
        """
        Verify create_response requires a result or error.
        """
        self.assertRaises(TypeError, handlers.create_response, UID)

    def test_create_response_with_result(self):
        """
        Verify create_response creates the proper result jsonrpc structure.
        """
        response = handlers.create_response(UID, result={'test': 'data'})
        self.assertEquals('2.0', response['jsonrpc'])
        self.assertEquals(UID, response['id'])
        self.assertEquals({'test': 'data'}, response['result'])

    def test_create_response_with_error(self):
        """
        Verify create_response creates the proper error jsonrpc structure.
        """
        for (error, expected_response) in [
            (Exception('test'), 'test'),
            ('test', 'test')
        ]:
            response = handlers.create_response(UID, error=error)
            self.assertEquals('2.0', response['jsonrpc'])
            self.assertEquals(UID, response['id'])
            print(response)
            self.assertEquals(expected_response, response['error']['message'])


class Test_return_error(TestCase):
    """
    Test for the return_error helper function.
    """

    def test_return_error(self):
        """
        Ensure return_error returns a proper error structure.
        """
        result = handlers.return_error({'id': UID}, Exception('test'), 1)
        self.assertEquals(1, result['error']['code'])
        self.assertEquals('test', result['error']['message'])
        self.assertEquals(str(Exception), result['error']['data']['exception'])
