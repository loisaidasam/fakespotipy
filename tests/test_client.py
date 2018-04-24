
import unittest

from fakespotipy import FakeSpotify


class BaseTestCase(object):
    def setUp(self):
        self.client = FakeSpotify()


class ClientBasicTests(BaseTestCase, unittest.TestCase):
    def test_no_responses(self):
        # Sanity
        self.assertEqual(self.client.responses, {})
        self.assertEqual(self.client.call_history, [])
        with self.assertRaises(NotImplementedError):
            self.client.refresh_access_token('foo')
        self.assertEqual(self.client.call_history, ['refresh_access_token'])
        with self.assertRaises(NotImplementedError):
            self.client.not_a_real_method()
        self.assertEqual(self.client.call_history,
                         ['refresh_access_token', 'not_a_real_method'])


class ClientMockResponseObjectTests(BaseTestCase, unittest.TestCase):
    def test_mock_response_object(self):
        # First, set up a mock response
        response = {
            'expires_in': 60,
            'access_token': 'BQDdKdI1eLRl2ErhCRC0jHdfr_DYEm_ecUuUPq2-dW_txQZeCrA32lNSYOZO7v7rEPXqC846nHlgSeg4m0c3-y05W9ISJRluCXdco4igf8eMhgLojXZb4RbE0vmlH4a06T3TX7Jg-uN1ClYFEkXnCGCA0NBNqkiFYDKlvMWqZExQom-XF-8pr6gV_PpzNJ2eKRRR6_ORp1ABUhtJ_aD8f5W4GexLq1mzpWQLkKE_Fq_LuwE1JhpxxNxRI-FLtzz46Jc',
            'token_type': 'Bearer',
            'refresh_token': 'AQDDNE-U4IElufFWfNjlwy7rOn-Kyt2PeIN1Nze2I5rVi7c9Etcx9blVkHVe5liSoKRMbJzS3etlA3sQ-0UqMKxRJ-HN08jrO_1IoDgciSZOaAUaQUiSkBOgtgnmO_tEHCU',
            'scope': 'user-top-read',
        }
        # Prep the client with that response
        self.client.add_response('refresh_access_token', response)
        # And trigger it
        response_actual = self.client.refresh_access_token('refresh_token_str_here')
        self.assertEqual(response, response_actual)
        self.assertEqual(self.client.call_history, ['refresh_access_token'])
        # If we try again, we get a NotImplementedError
        with self.assertRaises(NotImplementedError):
            self.client.refresh_access_token('refresh_token_str_here')
        self.assertEqual(self.client.call_history,
                         ['refresh_access_token', 'refresh_access_token'])


class CustomException(Exception):
    pass


class ClientMockResponseFunctionTests(BaseTestCase, unittest.TestCase):
    def setUp(self):
        super(ClientMockResponseFunctionTests, self).setUp()
        self.called_func_counter = 0

    def mock_refresh_response(self, refresh_token_str):
        """The mock function
        """
        self.called_func_counter += 1
        if refresh_token_str == 'foo':
            raise CustomException("Foo! Oh noes!")
        return {'foo': 'bar'}

    def test_mock_response_function(self):
        # Add it a couple of times (so we can call it twice)
        self.client.add_response('refresh_access_token',
                                 self.mock_refresh_response)
        self.client.add_response('refresh_access_token',
                                 self.mock_refresh_response)
        # Sanity
        self.assertEqual(self.called_func_counter, 0)
        self.assertEqual(self.client.call_history, [])
        # Call it once
        response = self.client.refresh_access_token('refresh_token_str_here')
        self.assertEqual(self.called_func_counter, 1)
        self.assertEqual(response, {'foo': 'bar'})
        self.assertEqual(self.client.call_history, ['refresh_access_token'])
        # Trigger again, using anticipated input to trigger custom Exception
        with self.assertRaises(CustomException):
            self.client.refresh_access_token('foo')
        self.assertEqual(self.called_func_counter, 2)
        self.assertEqual(self.client.call_history,
                         ['refresh_access_token', 'refresh_access_token'])
        # Try one more time, get NotImplementedError
        with self.assertRaises(NotImplementedError):
            self.client.refresh_access_token('foo')
        self.assertEqual(self.called_func_counter, 2)
        self.assertEqual(self.client.call_history, [
            'refresh_access_token',
            'refresh_access_token',
            'refresh_access_token',
        ])
