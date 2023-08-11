#!/usr/bin/python3
"""Defines unittests for class Amenity.
"""

import os
import unittest
from datetime import datetime
from time import sleep
from models.amenity import Amenity
import models


class TestAmenity(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp_file = "tmp_file.json"
        cls.orig_file = "file.json"
        os.rename(cls.orig_file, cls.tmp_file)

    @classmethod
    def tearDownClass(cls):
        os.rename(cls.tmp_file, cls.orig_file)

    def setUp(self):
        self.am = Amenity()

    def test_no_args_instantiates(self):
        self.assertEqual(Amenity, type(self.am))

    def test_new_instance_stored_in_objects(self):
        self.assertIn(self.am, models.storage.all().values())

    def test_id_is_public_str(self):
        am = Amenity()
        self.assertIsInstance(am.id, str)
        self.assertIsNotNone(am.id)

    def test_created_at_is_public_datetime(self):
        am = Amenity()
        self.assertIsInstance(am.created_at, datetime)

    def test_updated_at_is_public_datetime(self):
        am = Amenity()
        self.assertIsInstance(am.updated_at, datetime)

    def test_class_attributes(self):
        self.assertEqual(str, type(Amenity.name))
        self.assertIn("name", dir(Amenity()))
        self.assertNotIn("name", Amenity().__dict__)

    def test_two_amenities_unique_ids(self):
        am1 = Amenity()
        am2 = Amenity()
        self.assertNotEqual(am1.id, am2.id)

    def test_two_amenities_different_created_at(self):
        am1 = Amenity()
        sleep(0.10)
        am2 = Amenity()
        self.assertLess(am1.created_at, am2.created_at)

    def test_two_amenities_different_updated_at(self):
        am1 = Amenity()
        sleep(0.10)
        am2 = Amenity()
        self.assertLess(am1.updated_at, am2.updated_at)

    def test_one_save(self):
        am = Amenity()
        sleep(0.10)
        first_updated_at = am.updated_at
        am.save()
        self.assertLess(first_updated_at, am.updated_at)

    def test_two_saves(self):
        am = Amenity()
        sleep(0.10)
        first_updated_at = am.updated_at
        am.save()
        second_updated_at = am.updated_at
        sleep(0.10)
        am.save()
        self.assertLess(first_updated_at, second_updated_at)
        self.assertLess(second_updated_at, am.updated_at)

    def test_to_dict_type(self):
        am = Amenity()
        self.assertIsInstance(am.to_dict(), dict)

    def test_to_dict_contains_correct_keys(self):
        am = Amenity()
        keys = ["id", "created_at", "updated_at", "__class__"]
        for key in keys:
            self.assertIn(key, am.to_dict())

    def test_to_dict_datetime_attributes_are_strs(self):
        am = Amenity()
        am_dict = am.to_dict()
        self.assertEqual(str, type(am_dict["id"]))
        self.assertEqual(str, type(am_dict["created_at"]))
        self.assertEqual(str, type(am_dict["updated_at"]))

    def test_to_dict_output(self):
        am = Amenity()
        am.id = "123456"
        dt = datetime.today()
        am.created_at = am.updated_at = dt
        tdict = {
            'id': '123456',
            '__class__': 'Amenity',
            'created_at': dt.isoformat(),
            'updated_at': dt.isoformat(),
        }
        self.assertDictEqual(am.to_dict(), tdict)

    def test_contrast_to_dict_dunder_dict(self):
        am = Amenity()
        self.assertNotEqual(am.to_dict(), am.__dict__)

    def test_to_dict_with_arg(self):
        am = Amenity()
        with self.assertRaises(TypeError):
            am.to_dict(None)


if __name__ == "__main__":
    unittest.main()