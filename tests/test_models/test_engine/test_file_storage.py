#!/usr/bin/python3
"""Defines unittests for class file_storage.
"""

import os
import unittest
import models
from models.place import Place
from models.city import City
from models.amenity import Amenity
from models.review import Review
from models.base_model import BaseModel
from models.engine.file_storage import FileStorage
from models.user import User
from models.state import State


class TestFileStorage(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp_file = "tmp_file.json"
        cls.orig_file = "file.json"
        os.rename(cls.orig_file, cls.tmp_file)

    @classmethod
    def tearDownClass(cls):
        os.rename(cls.tmp_file, cls.orig_file)

    def setUp(self):
        self.file_storage = FileStorage()

    def test_FileStorage_instantiation(self):
        self.assertEqual(type(self.file_storage), FileStorage)

    def test_FileStorage_instantiation_no_args(self):
        self.assertIsInstance(FileStorage(), FileStorage)

    def test_FileStorage_instantiation_with_arg(self):
        with self.assertRaises(TypeError):
            FileStorage(None)

    def test_FileStorage_file_path_is_private_str(self):
        file_storage = FileStorage()
        self.assertIsInstance(file_storage._FileStorage__file_path, str)

    def testFileStorage_objects_is_private_dict(self):
        file_storage = FileStorage()
        self.assertIsInstance(file_storage._FileStorage__objects, dict)

    def test_storage_initializes(self):
        self.assertIsInstance(models.storage, FileStorage)

    def test_all(self):
        self.assertIsInstance(models.storage.all(), dict)

    def test_all_with_arg(self):
        with self.assertRaises(TypeError):
            models.storage.all(None)

    def test_new(self):
        bm = BaseModel()
        us = User()
        st = State()
        pl = Place()
        cy = City()
        am = Amenity()
        rv = Review()
        models.storage.new(bm)
        models.storage.new(us)
        models.storage.new(st)
        models.storage.new(pl)
        models.storage.new(cy)
        models.storage.new(am)
        models.storage.new(rv)
        self.assertIn("BaseModel." + bm.id, models.storage.all())
        self.assertIn(bm, models.storage.all().values())
        self.assertIn("User." + us.id, models.storage.all())
        self.assertIn(us, models.storage.all().values())
        self.assertIn("State." + st.id, models.storage.all())
        self.assertIn(st, models.storage.all().values())
        self.assertIn("Place." + pl.id, models.storage.all())
        self.assertIn(pl, models.storage.all().values())
        self.assertIn("City." + cy.id, models.storage.all())
        self.assertIn(cy, models.storage.all().values())
        self.assertIn("Amenity." + am.id, models.storage.all())
        self.assertIn(am, models.storage.all().values())
        self.assertIn("Review." + rv.id, models.storage.all())
        self.assertIn(rv, models.storage.all().values())

    def test_new_with_args(self):
        with self.assertRaises(TypeError):
            models.storage.new(BaseModel(), 1)

    def test_save(self):
        bm = BaseModel()
        us = User()
        st = State()
        pl = Place()
        cy = City()
        am = Amenity()
        rv = Review()
        models.storage.new(bm)
        models.storage.new(us)
        models.storage.new(st)
        models.storage.new(pl)
        models.storage.new(cy)
        models.storage.new(am)
        models.storage.new(rv)
        models.storage.save()
        with open("file.json", "r") as file:
            save_text = file.read()
            self.assertIn("BaseModel." + bm.id, save_text)
            self.assertIn("User." + us.id, save_text)
            self.assertIn("State." + st.id, save_text)
            self.assertIn("Place." + pl.id, save_text)
            self.assertIn("City." + cy.id, save_text)
            self.assertIn("Amenity." + am.id, save_text)
            self.assertIn("Review." + rv.id, save_text)

    def test_save_with_arg(self):
        with self.assertRaises(TypeError):
            models.storage.save(None)

    def test_reload(self):
        bm = BaseModel()
        us = User()
        st = State()
        pl = Place()
        cy = City()
        am = Amenity()
        rv = Review()
        models.storage.new(bm)
        models.storage.new(us)
        models.storage.new(st)
        models.storage.new(pl)
        models.storage.new(cy)
        models.storage.new(am)
        models.storage.new(rv)
        models.storage.save()
        models.storage.reload()
        objs = FileStorage._FileStorage__objects
        self.assertIn("BaseModel." + bm.id, objs)
        self.assertIn("User." + us.id, objs)
        self.assertIn("State." + st.id, objs)
        self.assertIn("Place." + pl.id, objs)
        self.assertIn("City." + cy.id, objs)
        self.assertIn("Amenity." + am.id, objs)
        self.assertIn("Review." + rv.id, objs)

    def test_reload_with_arg(self):
        with self.assertRaises(TypeError):
            models.storage.reload(None)


if __name__ == "__main__":
    unittest.main()