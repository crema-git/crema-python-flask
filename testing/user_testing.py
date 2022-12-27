import unittest
import os
import json
from app import app


class UserTesting(unittest.TestCase):

    def setUp(self) -> None:
        """Define test variables and initialize app."""
        self.app = app
        self.client = self.app.test_client()

    def test_registration(self):
        # Given
        name = "paurakh"
        email = "paurakh011@gmail.com"
        password = "mycoolpassword"

        payload = json.dumps({
            "name": name,
            "email": email,
            "password": password
        })

        """Test API can create a bucketlist (POST request)"""
        res = self.client().post('/api/users', data=payload)
        self.assertEqual(res.status_code, 200)

    def test_login(self):
        # Given
        email = "paurakh011@gmail.com"
        password = "mycoolpassword"

        payload = json.dumps({
            "email": email,
            "password": password
        })

        """Test API can create a bucketlist (POST request)"""
        res = self.client().post('/api/auth', data=payload)
        self.assertEqual(res.status_code, 200)
