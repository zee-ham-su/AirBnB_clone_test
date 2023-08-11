#!/usr/bin/python3
"""Defines unittests for class Base_model.
"""
import unittest
import os
from datetime import datetime
from time import sleep
from models.base_model import BaseModel
import models
from unittest.mock import patch


class TestBaseModel(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp_file = "tmp_file.json"
        cls.orig_file = "file.json"
        os.rename(cls.orig_file, cls.tmp_file)

    @classmethod
    def tearDownClass(cls):
        os.rename(cls.tmp_file, cls.orig_file)

    def setUp(self):
        self.bm = BaseModel()

    def test_no_args_instantiates(self):
        self.assertEqual(BaseModel, type(self.bm))

    def test_new_instance_stored_in_objects(self):
        self.assertIn(self.bm, models.storage.all().values())

    def test_args_unused(self):
        bm = BaseModel(None)
        unused_args = [arg for arg in bm.__dict__.values() if arg is None]
        self.assertEqual(len(unused_args), 0, "Some arguments were left unused.")

    def test_id_is_public_str(self):
        bm = BaseModel()
        self.assertIsInstance(bm.id, str)
        self.assertIsNotNone(bm.id)

    def test_created_at_is_public_datetime(self):
        bm = BaseModel()
        self.assertIsInstance(bm.created_at, datetime)

    def test_updated_at_is_public_datetime(self):
        bm = BaseModel()
        self.assertIsInstance(bm.updated_at, datetime)

    def test_two_models_unique_ids(self):
        bm1 = BaseModel()
        bm2 = BaseModel()
        self.assertNotEqual(bm1.id, bm2.id)

    def test_two_models_different_created_at(self):
        bm1 = BaseModel()
        sleep(0.10)
        bm2 = BaseModel()
        self.assertLess(bm1.created_at, bm2.created_at)

    def test_two_models_different_updated_at(self):
        bm1 = BaseModel()
        sleep(0.10)
        bm2 = BaseModel()
        self.assertLess(bm1.updated_at, bm2.updated_at)

    def test_to_dict_type(self):
        bm = BaseModel()
        self.assertIsInstance(bm.to_dict(), dict)

    def test_to_dict_contains_correct_keys(self):
        bm = BaseModel()
        keys = ["id", "created_at", "updated_at", "__class__"]
        for key in keys:
            self.assertIn(key, bm.to_dict())

    def test_to_dict_datetime_attributes_are_strs(self):
        bm = BaseModel()
        bm_dict = bm.to_dict()
        self.assertEqual(str, type(bm_dict["id"]))
        self.assertEqual(str, type(bm_dict["created_at"]))
        self.assertEqual(str, type(bm_dict["updated_at"]))

    def test_to_dict_output(self):
        bm = BaseModel()
        bm.id = "123456"
        dt = datetime.today()
        bm.created_at = bm.updated_at = dt
        tdict = {
            'id': '123456',
            '__class__': 'BaseModel',
            'created_at': dt.isoformat(),
            'updated_at': dt.isoformat(),
        }
        self.assertDictEqual(bm.to_dict(), tdict)

    def test_contrast_to_dict_dunder_dict(self):
        bm = BaseModel()
        self.assertNotEqual(bm.to_dict(), bm.__dict__)

    def test_to_dict_with_arg(self):
        bm = BaseModel()
        with self.assertRaises(TypeError):
            bm.to_dict(None)

    def test_one_save(self):
        bm = BaseModel()
        sleep(0.10)
        first_updated_at = bm.updated_at
        bm.save()
        self.assertLess(first_updated_at, bm.updated_at)

    def test_two_saves(self):
        bm = BaseModel()
        sleep(0.10)
        first_updated_at = bm.updated_at
        bm.save()
        second_updated_at = bm.updated_at
        sleep(0.10)
        bm.save()
        self.assertLess(first_updated_at, second_updated_at)
        self.assertLess(second_updated_at, bm.updated_at)

    def test_save_updates_file(self):
        self.bm.save()
        bmid = "BaseModel." + self.bm.id
        with open("file.json", "r") as file:
            self.assertIn(bmid, file.read())


if __name__ == '__main__':
    unittest.main()
