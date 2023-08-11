#!/usr/bin/python3
"""Defines unittests for models/place.py.
"""

import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.place import Place
from models.engine.file_storage import FileStorage
from models import storage


class TestPlace(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp_file = "tmp_file.json"
        cls.orig_file = "file.json"
        os.rename(cls.orig_file, cls.tmp_file)

    @classmethod
    def tearDownClass(cls):
        os.rename(cls.tmp_file, cls.orig_file)

    def setUp(self):
        self.pl = Place()

    def test_new_instance_stored_in_objects(self):
        self.assertIn(Place(), models.storage.all().values())

    def test_id_is_public_str(self):
        pl = Place()
        self.assertIsInstance(pl.id, str)
        self.assertIsNotNone(pl.id)

    def test_created_at_is_public_datetime(self):
        pl = Place()
        self.assertIsInstance(pl.created_at, datetime)

    def test_updated_at_is_public_datetime(self):
        pl = Place()
        self.assertIsInstance(pl.updated_at, datetime)

    def test_two_places_different_created_at(self):
        pl1 = Place()
        sleep(0.05)
        pl2 = Place()
        self.assertTrue(pl2.created_at > pl1.created_at)

    def test_two_places_different_updated_at(self):
        pl1 = Place()
        sleep(0.05)
        pl2 = Place()
        self.assertTrue(pl2.updated_at > pl1.updated_at)

    def test_args_unused(self):
        pl = Place(None)
        self.assertNotIn(None, pl.__dict__.values())

    def test_class_attributes(self):
        pl = Place()
        self.assertEqual(str, type(pl.city_id))
        self.assertEqual(str, type(pl.user_id))
        self.assertEqual(str, type(pl.name))
        self.assertEqual(str, type(pl.description))
        self.assertEqual(int, type(pl.number_rooms))
        self.assertEqual(int, type(pl.number_bathrooms))
        self.assertEqual(int, type(pl.max_guest))
        self.assertEqual(int, type(pl.price_by_night))
        self.assertEqual(float, type(pl.latitude))
        self.assertEqual(float, type(pl.longitude))
        self.assertEqual(list, type(pl.amenity_ids))

    def test_one_save(self):
        pl = Place()
        first_updated_at = pl.updated_at
        sleep(0.05)
        pl.save()
        self.assertLess(first_updated_at, pl.updated_at)

    def test_two_saves(self):
        pl = Place()
        first_updated_at = pl.updated_at
        sleep(0.05)
        pl.save()
        second_updated_at = pl.updated_at
        sleep(0.05)
        pl.save()
        self.assertLess(first_updated_at, second_updated_at)
        self.assertLess(second_updated_at, pl.updated_at)

    def test_save_with_arg(self):
        pl = Place()
        with self.assertRaises(TypeError):
            pl.save(None)

    def test_save_updates_file(self):
        pl = Place()
        pl.save()
        storage.reload()
        plid = "Place." + pl.id
        with open("file.json", "r") as file:
            content = file.read()
            self.assertIn(plid, content)

        storage.reload()
        self.assertTrue(plid in storage.all())

    def test_to_dict_type(self):
        pl = Place()
        self.assertIsInstance(pl.to_dict(), dict)

    def test_to_dict_contains_correct_keys(self):
        pl = Place()
        keys = ["id", "created_at", "updated_at", "__class__"]
        for key in keys:
            self.assertIn(key, pl.to_dict())

    def test_to_dict_datetime_attributes_are_strs(self):
        pl = Place()
        pl_dict = pl.to_dict()
        self.assertEqual(str, type(pl_dict["id"]))
        self.assertEqual(str, type(pl_dict["created_at"]))
        self.assertEqual(str, type(pl_dict["updated_at"]))

    def test_to_dict_output(self):
        pl = Place()
        pl.id = "123456"
        dt = datetime.today()
        pl.created_at = pl.updated_at = dt
        tdict = {
            'id': '123456',
            '__class__': 'Place',
            'created_at': dt.isoformat(),
            'updated_at': dt.isoformat(),
        }
        self.assertDictEqual(pl.to_dict(), tdict)

    def test_contrast_to_dict_dunder_dict(self):
        pl = Place()
        self.assertNotEqual(pl.to_dict(), pl.__dict__)

    def test_to_dict_with_arg(self):
        pl = Place()
        with self.assertRaises(TypeError):
            pl.to_dict(None)


if __name__ == "__main__":
    unittest.main()