#!/usr/bin/python3
"""Defines unittests for models/review.py.
"""


import os
import unittest
from datetime import datetime, timedelta
from time import sleep
from models.review import Review
import models


class TestReview(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp_file = "tmp_file.json"
        cls.orig_file = "file.json"
        os.rename(cls.orig_file, cls.tmp_file)

    @classmethod
    def tearDownClass(cls):
        os.rename(cls.tmp_file, cls.orig_file)

    def setUp(self):
        self.rv = Review()

    def test_no_args_instantiates(self):
        self.assertEqual(Review, type(self.rv))

    def test_new_instance_stored_in_objects(self):
        self.assertIn(self.rv, models.storage.all().values())

    def test_str_representation_contains_class_name(self):
        rvstr = self.rv.__str__()
        self.assertIn("[Review]", rvstr)

    def test_two_reviews_unique_ids(self):
        rv2 = Review()
        self.assertNotEqual(self.rv.id, rv2.id)

    def test_two_reviews_different_created_at(self):
        rv2 = Review()
        sleep(0.10)
        self.assertLess(self.rv.created_at, rv2.created_at)

    def test_two_reviews_different_updated_at(self):
        rv2 = Review()
        sleep(0.10)
        self.assertLess(self.rv.updated_at, rv2.updated_at)

    def test_update_attributes(self):
        self.rv.place_id = "test_place_id"
        self.rv.user_id = "test_user_id"
        self.rv.text = "This is a test review."
        self.assertEqual("test_place_id", self.rv.place_id)
        self.assertEqual("test_user_id", self.rv.user_id)
        self.assertEqual("This is a test review.", self.rv.text)

    def test_save(self):
        first_updated_at = self.rv.updated_at
        self.rv.save()
        self.assertLess(first_updated_at, self.rv.updated_at)

    def test_save_updates_file(self):
        self.rv.save()
        rvid = "Review." + self.rv.id
        with open("file.json", "r") as f:
            self.assertIn(rvid, f.read())

    def test_updated_at_after_save(self):
        original_updated_at = self.rv.updated_at
        sleep(0.05)
        self.rv.save()
        self.assertLess(original_updated_at, self.rv.updated_at)

    def test_to_dict_with_arg(self):
        """Test that calling to_dict with an argument raises TypeError."""
        with self.assertRaises(TypeError):
            review_instance = Review()
            review_instance.to_dict(None)

    def test_contrast_to_dict_dunder_dict(self):
        """Test that the dictionary from to_dict is different from __dict__."""
        review_instance = Review()

        to_dict_dict = review_instance.to_dict()
        instance_dict = review_instance.__dict__

        self.assertIsNot(to_dict_dict, instance_dict)

    def test_to_dict(self):
        dt = datetime.today()
        self.rv.id = "123456"
        self.rv.created_at = self.rv.updated_at = dt
        tdict = {
            'id': '123456',
            '__class__': 'Review',
            'created_at': dt.isoformat(),
            'updated_at': dt.isoformat(),
        }
        self.assertDictEqual(self.rv.to_dict(), tdict)

    def test_datetime_format_in_to_dict(self):
        dt = datetime.today()
        self.rv.id = "123456"
        self.rv.created_at = dt
        self.rv.updated_at = dt + timedelta(days=1)
        rv_dict = self.rv.to_dict()
        self.assertEqual(dt.isoformat(), rv_dict["created_at"])
        self.assertEqual((dt + timedelta(days=1)).isoformat(), rv_dict["updated_at"])

    def test_save_with_arg(self):
        """Test that calling save with an argument raises TypeError."""
        def save_with_arg():
            review_instance = Review()
            review_instance.save(None)

        self.assertRaises(TypeError, save_with_arg)


if __name__ == "__main__":
    unittest.main()
