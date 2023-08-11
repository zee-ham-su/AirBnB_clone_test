#!/usr/bin/python3
"""Defines unittests for models/user.py.
"""
import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.user import User


class TestUser(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp_file = "tmp_file.json"
        cls.orig_file = "file.json"
        os.rename(cls.orig_file, cls.tmp_file)

    @classmethod
    def tearDownClass(cls):
        os.rename(cls.tmp_file, cls.orig_file)

    def setUp(self):
        self.us = User()

    def test_empty_strings_for_attributes(self):
        self.assertEqual("", self.us.email)
        self.assertEqual("", self.us.password)
        self.assertEqual("", self.us.first_name)
        self.assertEqual("", self.us.last_name)

    def test_default_values_for_optional_attributes(self):
        self.assertEqual("", self.us.email)
        self.assertEqual("", self.us.password)
        self.assertEqual("", self.us.first_name)
        self.assertEqual("", self.us.last_name)

    def test_first_name_is_public_str(self):
        self.assertEqual(str, type(User.first_name))

    def test_last_name_is_public_str(self):
        self.assertEqual(str, type(User.last_name))

    def test_password_is_public_str(self):
        self.assertEqual(str, type(User.password))

    def test_email_is_public_str(self):
        self.assertEqual(str, type(User.email))

    def test_two_users_unique_ids(self):
        us2 = User()
        self.assertNotEqual(self.us.id, us2.id)

    def test_two_users_different_created_at(self):
        us2 = User()
        sleep(0.10)
        self.assertLess(self.us.created_at, us2.created_at)

    def test_two_users_different_updated_at(self):
        us2 = User()
        sleep(0.10)
        self.assertLess(self.us.updated_at, us2.updated_at)

    def test_save(self):
        first_updated_at = self.us.updated_at
        self.us.save()
        self.assertLess(first_updated_at, self.us.updated_at)

    def test_save_updates_file(self):
        us = User()
        us.save()
        usid = "User." + us.id
        with open("file.json", "r") as file:
            self.assertIn(usid, file.read())

    def test_save_updates_file(self):
        self.us.save()
        usid = "User." + self.us.id
        with open("file.json", "r") as f:
            self.assertIn(usid, f.read())

    def test_to_dict(self):
        dt = datetime.today()
        self.us.id = "123456"
        self.us.created_at = self.us.updated_at = dt
        tdict = {
            'id': '123456',
            '__class__': 'User',
            'created_at': dt.isoformat(),
            'updated_at': dt.isoformat(),
        }
        self.assertDictEqual(self.us.to_dict(), tdict)

    def test_to_dict_with_arg(self):
        us = User()
        with self.assertRaises(TypeError):
            us.to_dict(None)

    def test_to_dict_contains_added_attributes(self):
        us = User()
        us.middle_name = "Alx"
        us.my_number = 45
        self.assertEqual("Alx", us.middle_name)
        self.assertIn("my_number", us.to_dict())


if __name__ == "__main__":
    unittest.main()
