#!/usr/bin/python3
""" Unittest mod. for the User Class"""

import unittest
from datetime import datetime
from time import sleep
from models.user import User, BaseModel


class TestUser(unittest.TestCase):
    """Test suite for the User class."""

    def test_user_inherits_from_base_model(self):
        """Test if User class inherits from BaseModel class."""
        self.assertTrue(issubclass(User, BaseModel))

    def test_user_attributes_exist(self):
        """Test if the required attributes exist in User instances."""
        user = User()
        self.assertTrue(hasattr(user, 'email'))
        self.assertTrue(hasattr(user, 'password'))
        self.assertTrue(hasattr(user, 'first_name'))
        self.assertTrue(hasattr(user, 'last_name'))

    def test_user_attributes_initial_values(self):
        """Test if User instance attributes have correct initial
        values."""
        user = User()
        self.assertEqual(user.email, "")
        self.assertEqual(user.password, "")
        self.assertEqual(user.first_name, "")
        self.assertEqual(user.last_name, "")

    def test_user_attributes_type(self):
        """Test if User instance attributes have the correct
        data types."""
        user = User()
        self.assertIsInstance(user.email, str)
        self.assertIsInstance(user.password, str)
        self.assertIsInstance(user.first_name, str)
        self.assertIsInstance(user.last_name, str)

    def test_user_creation_date(self):
        """Test if User instance has valid creation and update
        date attributes."""
        user = User()
        self.assertIsInstance(user.created_at, datetime)
        self.assertIsInstance(user.updated_at, datetime)

    def test_user_save_updates_updated_at(self):
        """Test if calling save() updates the 'updated_at'
        attribute."""
        user = User()
        sleep(0.05)
        first_updated_at = user.updated_at
        user.save()
        self.assertLess(first_updated_at, user.updated_at)

    def test_user_to_dict(self):
        """Test if User instance's to_dict() method returns a
        valid dictionary."""
        user = User()
        user.id = "123"
        user.created_at = user.updated_at = datetime(2023, 8, 8, 12, 0, 0)
        user_dict = user.to_dict()
        self.assertEqual(user_dict['__class__'], 'User')
        self.assertEqual(user_dict['id'], '123')
        self.assertEqual(user_dict['created_at'], '2023-08-08T12:00:00')
        self.assertEqual(user_dict['updated_at'], '2023-08-08T12:00:00')


if __name__ == '__main__':
    unittest.main()
