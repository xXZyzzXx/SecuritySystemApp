import unittest
import json
import random

from server import app
from encrypt import encrypt_message, decrypt_message


class TestAlarm(unittest.TestCase):

    def setUp(self):
        self.app = app  # Need to change force_https to False
        self.app.config['TESTING'] = True
        self.client = app.test_client()
        self.data = {'status': 'reload'}
        self.app_id = 1234

    def test_successful_encrypt(self):
        # Given
        encrypted = encrypt_message(self.data)

        response = self.client.post(f'/api/alarm/{self.app_id}', data=encrypted)  # Return None, 302 Error

        r = response.json()
        decrypt = decrypt_message(r['key'].encode())
        answer = json.loads(decrypt)
        # Then
        self.assertEqual(response.status_code, 200)
        self.assertEqual(answer['command'], 'reload')

    def tearDown(self):
        pass
