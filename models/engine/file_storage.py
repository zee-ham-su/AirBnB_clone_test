#!/usr/bin/python3
"""
 class FileStorage that serializes instances to a JSON file and deserializes JSON file to instances
"""

import json
from os.path import exists


class FileStorage:
    """Serializes instances to a JSON file and deserializes JSON file to instances"""

    __file_path = "file.json"
    __objects = {}

    def all(self):
        """Returns the dictionary __objects"""
        return FileStorage.__objects

    def new(self, obj):
        """Sets in __objects the obj with key <obj class name>.id"""
        key = f"{obj.__class__.__name__}.{obj.id}"
        FileStorage.__objects[key] = obj

    def save(self):
        """Serializes __objects to the JSON file (path: __file_path)"""
        obj_dict = {key: obj.to_dict()
                              for key, obj in FileStorage.__objects.items()}
        with open(FileStorage.__file_path, "w") as file:
            json.dump(obj_dict, file)

    def reload(self):
        """Deserializes the JSON file to __objects (only if the JSON file (__file_path) exists)"""
        if exists(FileStorage.__file_path):
            with open(FileStorage.__file_path, "r") as file:
                data = json.load(file)
                for key, obj_data in data.items():
                    class_name, obj_id = key.split('.')
                    module = __import__(class_name)
                    class_ = getattr(module, class_name)
                    instance = class_(**obj_data)
                    FileStorage.__objects[key] = instance
