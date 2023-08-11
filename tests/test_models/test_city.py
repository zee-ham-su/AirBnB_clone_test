#!/usr/bin/python3
"""Defines unittests for Class City.
"""

import os
import unittest
from datetime import datetime
from time import sleep
from models.city import City
import models


class TestCity(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp_file = "tmp_file.json"
        cls.orig_file = "file.json"
        os.rename(cls.orig_file, cls.tmp_file)

    @classmethod
    def tearDownClass(cls):
        os.rename(cls.tmp_file, cls.orig_file)

    def setUp(self):
        self.cy = City()

    def test_id_is_public_str(self):
        cy = City()
        self.assertIsInstance(cy.id, str)
        self.assertIsNotNone(cy.id)

    def test_no_args_instantiates(self):
        self.assertEqual(City, type(self.cy))

    def test_new_instance_stored_in_objects(self):
        self.assertIn(self.cy, models.storage.all().values())

    def test_created_at_is_public_datetime(self):
        cy = City()
        self.assertIsInstance(cy.created_at, datetime)

    def test_updated_at_is_public_datetime(self):
        cy = City()
        self.assertIsInstance(cy.updated_at, datetime)

    def test_class_attributes(self):
        cy = City()
        self.assertEqual(str, type(cy.state_id))
        self.assertEqual(str, type(cy.name))

    def test_two_cities_unique_ids(self):
        cy1 = City()
        cy2 = City()
        self.assertNotEqual(cy1.id, cy2.id)

    def test_two_cities_different_created_at(self):
        cy1 = City()
        sleep(0.05)
        cy2 = City()
        self.assertLess(cy1.created_at, cy2.created_at)

    def test_two_cities_different_updated_at(self):
        cy1 = City()
        sleep(0.05)
        cy2 = City()
        self.assertLess(cy1.updated_at, cy2.updated_at)

    def test_one_save(self):
        cy = City()
        first_updated_at = cy.updated_at
        sleep(0.05)
        cy.save()
        self.assertLess(first_updated_at, cy.updated_at)

    def test_two_saves(self):
        cy = City()
        first_updated_at = cy.updated_at
        sleep(0.05)
        cy.save()
        second_updated_at = cy.updated_at
        sleep(0.05)
        cy.save()
        self.assertLess(first_updated_at, second_updated_at)
        self.assertLess(second_updated_at, cy.updated_at)

    def test_save_updates_file(self):
        self.cy.save()
        cyid = "City." + self.cy.id
        with open("file.json", "r") as file:
            self.assertIn(cyid, file.read())

    def test_to_dict_type(self):
        cy = City()
        self.assertIsInstance(cy.to_dict(), dict)

    def test_to_dict_contains_correct_keys(self):
        cy = City()
        keys = ["id", "created_at", "updated_at", "__class__"]
        for key in keys:
            self.assertIn(key, cy.to_dict())

    def test_to_dict_datetime_attributes_are_strs(self):
        cy = City()
        cy_dict = cy.to_dict()
        self.assertEqual(str, type(cy_dict["id"]))
        self.assertEqual(str, type(cy_dict["created_at"]))
        self.assertEqual(str, type(cy_dict["updated_at"]))

    def test_to_dict_output(self):
        cy = City()
        cy.id = "123456"
        dt = datetime.today()
        cy.created_at = cy.updated_at = dt
        tdict = {
            'id': '123456',
            '__class__': 'City',
            'created_at': dt.isoformat(),
            'updated_at': dt.isoformat(),
        }
        self.assertDictEqual(cy.to_dict(), tdict)

    def test_contrast_to_dict_dunder_dict(self):
        cy = City()
        self.assertNotEqual(cy.to_dict(), cy.__dict__)

    def test_to_dict_with_arg(self):
        cy = City()
        with self.assertRaises(TypeError):
            cy.to_dict(None)


if __name__ == '__main__':
    unittest.main()
