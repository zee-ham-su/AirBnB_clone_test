#!/usr/bin/python3
"""
class FileStorage that serializes instances to a
JSON file and deserializes JSON file to instances
"""
from models.base_model import BaseModel
import json
import os
from models.user import User
from models.amenity import Amenity
from models.review import Review
from models.place import Place
from models.state import State
from models.city import City


class FileStorage:
    """Serializes instances to a JSON file and deserializes
    JSON file to instances"""

    __file_path = "file.json"
    __objects = {}
    classes = {
        'BaseModel': BaseModel,
        'User': User,
        'Amenity': Amenity,
        'Review': Review,
        'Place': Place,
        'State': State,
        'City': City
    }

    def get_instance_by_id(self, cls_name, instance_id):
        """Retrieves an instance by class name and ID"""
        key = f"{cls_name}.{instance_id}"
        return FileStorage.__objects.get(key)

    def all(self):
        """Returns the dictionary __objects"""
        return FileStorage.__objects

    def new(self, obj):
        """Sets in __objects the obj with key <obj
        class name>.id
        """
        key = f"{obj.__class__.__name__}.{obj.id}"
        FileStorage.__objects[key] = obj

    def save(self):
        """Serializes __objects to the JSON file
        (path: __file_path)
        """
        obj_dict = {key: obj.to_dict()
                    for key, obj in FileStorage.__objects.items()}
        with open(FileStorage.__file_path, "w") as file:
            json.dump(obj_dict, file)

    def reload(self):
        """Deserializes the JSON file to __objects (only
        if the JSON file exists)"""
        if os.path.exists(FileStorage.__file_path):
            with open(FileStorage.__file_path, 'r') as file:
                obj_dict = json.load(file)
            for key, value in obj_dict.items():
                cls_name = value['__class__']
                cls = FileStorage.classes.get(cls_name)
                if cls:
                    instance = cls(**value)
                    self.new(instance)
