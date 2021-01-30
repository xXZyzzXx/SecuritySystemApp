import unittest
import json
import random

from server import app
from encrypt import encrypt_message, decrypt_message


class TestAlarm(unittest.TestCase):

    def setUp(self):
        self.app = app
        self.app.config['TESTING'] = True
        self.client = app.test_client()
        self.data = {'alarm': 'caution'}
        self.app_id = random.randint(1000, 9999)

    def test_successful_encrypt(self):
        encrypted = encrypt_message(self.data)
        response = self.client.post(f'/api/alarm/{self.app_id}', data={"key": encrypted})
        r = response.get_json()
        decrypt = decrypt_message(r['key'].encode())
        answer = json.loads(decrypt)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(answer['command'], 'reload')

    def tearDown(self):
        pass
