#!/usr/bin/python3
"""Defines unittests for models/state.py.
"""

import os
import unittest
from datetime import datetime
from time import sleep
from models.state import State
import models
from models.engine.file_storage import FileStorage
from models import storage
from models.base_model import BaseModel


class TestState(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp_file = "tmp_file.json"
        cls.orig_file = "file.json"
        os.rename(cls.orig_file, cls.tmp_file)

    @classmethod
    def tearDownClass(cls):
        os.rename(cls.tmp_file, cls.orig_file)

    def setUp(self):
        self.st = State()

    def test_no_args_instantiates(self):
        self.assertEqual(State, type(self.st))

    def test_new_instance_stored_in_objects(self):
        self.assertIn(self.st, models.storage.all().values())

    def test_instantiation_with_None_kwargs(self):
        with self.assertRaises(TypeError):
            State(id=None, created_at=None, updated_at=None)

    def test_instantiation(self):
        """Tests instantiation of State class."""
        state_instance = State()

        self.assertTrue(isinstance(state_instance, State))
        self.assertTrue(isinstance(state_instance, BaseModel))

    def test_two_states_unique_ids(self):
        st2 = State()
        self.assertNotEqual(self.st.id, st2.id)

    def test_two_states_different_created_at(self):
        st2 = State()
        sleep(0.15)
        self.assertLess(self.st.created_at, st2.created_at)

    def test_two_states_different_updated_at(self):
        st2 = State()
        sleep(0.15)
        self.assertLess(self.st.updated_at, st2.updated_at)

    def test_attributes(self):
        """Tests the attributes of State class."""
        state_instance = State()
        for attribute in dir(state_instance):
            if not attribute.startswith("__"):
                attribute_type = type(getattr(state_instance, attribute))
                with self.subTest(attribute=attribute):
                    self.assertTrue(hasattr(state_instance, attribute))
                    self.assertIsInstance(getattr(state_instance, attribute), attribute_type)

    def test_save(self):
        first_updated_at = self.st.updated_at
        self.st.save()
        self.assertLess(first_updated_at, self.st.updated_at)

    def test_save_updates_file(self):
        self.st.save()
        stid = "State." + self.st.id
        with open("file.json", "r") as file:
            self.assertIn(stid, file.read())

    def test_to_dict(self):
        dt = datetime.today()
        self.st.id = "123456"
        self.st.created_at = self.st.updated_at = dt
        tdict = {
            'id': '123456',
            '__class__': 'State',
            'created_at': dt.isoformat(),
            'updated_at': dt.isoformat(),
        }
        self.assertDictEqual(self.st.to_dict(), tdict)

    def test_to_dict_type(self):
        self.assertTrue(dict, type(State().to_dict()))

    def test_to_dict_with_arg(self):
        st = State()
        with self.assertRaises(TypeError):
            st.to_dict(None)


if __name__ == "__main__":
    unittest.main()
