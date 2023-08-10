#!/usr/bin/python3
"""
a program called console.py that contains the entry point of
the command interpreter
"""
import cmd
import re
import json
from models.base_model import BaseModel
from models.engine.file_storage import FileStorage
from models.user import User
from models.place import Place
from models.amenity import Amenity
from models.review import Review
from models.state import State
from models.city import City
from models import storage


class HBNBCommand(cmd.Cmd):
    """Defines the command interpreter
    Attributes:
        prompt (str): The command prompt.
    """

    prompt = "(hbnb) "
    __classes = {
        "BaseModel": BaseModel,
        "User": User,
        "State": State,
        "City": City,
        "Place": Place,
        "Amenity": Amenity,
        "Review": Review
    }

    def default(self, user_input):
        """The standard response of the cmd module when the input
        provided is not valid."""
        argdict = {
            "all": self.do_all,
            "show": self.do_show,
            "destroy": self.do_destroy,
            "count": self.do_count,
            "update": self.do_update
        }
        match = re.search(r"^(\w*)\.(\w+)(?:\(([^)]*)\))$", user_input)
        if match:
            class_name, method, user_input = match.groups()

            if class_name in self.__classes:
                command = "{} {}".format(class_name, user_input)
                if method in argdict:
                    return argdict[method](command)
                print("Method '{}' unrecognized for class '{}'".format(method, class_name))
            else:
                print("** class doesn't exist **")
        else:
            print("Invalid command")
        return False

    def do_quit(self, user_input):
        """Quit command to exit the program"""
        return True

    def do_EOF(self, user_input):
        """Exit the program using Ctrl+D"""
        print()
        return True

    def emptyline(self):
        """Do nothing on an empty line"""
        pass

    def do_create(self, user_input):
        """ Creates a new instance of BaseModel, saves it
        (to the JSON file) and prints the id
        """
        if not user_input:
            print("** class name missing **")
            return
        args = user_input.split()
        class_name = args[0]
        if class_name not in FileStorage.classes.keys():
            print("** class doesn't exist **")
            return

        new_instance = FileStorage.classes[class_name]()
        new_instance.save()
        print(new_instance.id)

    def do_show(self, user_input):
        """Shows the string representation of an instance"""
        if not user_input:
            print("** class name missing **")
            return
        args = user_input.split()
        if len(args) < 2:
            print("** instance id missing **")
            return

        cls_name = args[0]
        instance_id = args[1].strip()

        if cls_name not in FileStorage.classes:
            print("** class doesn't exist **")
            return
        if instance_id.startswith('"') and instance_id.endswith('"'):
            instance_id = instance_id[1:-1]

        storage = FileStorage()
        instance = storage.get_instance_by_id(cls_name, instance_id)

        if instance is None:
            print("** no instance found **")
            return

        print(instance)

    def do_destroy(self, user_input):
        """Delete an instance based on the class name and id"""
        if not user_input:
            print("** class name missing **")
            return
        args = user_input.split()
        class_name = args[0]
        if class_name not in storage.classes:
            print("** class doesn't exist **")
            return
        if len(args) < 2:
            print("** instance id missing **")
            return
        instance_id = args[1]
        all_instances = storage.all()
        instance_key = f"{class_name}.{instance_id}"
        if instance_key not in all_instances:
            print("** no instance found **")
            return
        all_instances.pop(instance_key)
        storage.save()

    def do_all(self, user_input):
        """Print string representations of all instances"""
        args = user_input.split()
        if args and args[0] not in storage.classes:
            print("** class doesn't exist **")
            return
        all_instances = storage.all()
        result = []
        for key, instance in all_instances.items():
            if not args or instance.__class__.__name__ == args[0]:
                result.append(str(instance))
        print(result)

    def do_update(self, user_input):
        """Update an instance based on the class name, id, and
        dictionary representation"""
        args = user_input.split()
        if len(args) < 4:
            print("** class name missing **")
            return
        class_name = args[0]
        if class_name not in self.__classes:
            print("** class doesn't exist **")
            return
        if len(args) < 2:
            print("** instance id missing **")
            return
        instance_id = args[1]
        instance_id = instance_id.strip('"')
        all_instances = storage.all()
        instance_key = f"{class_name}.{instance_id}"
        if instance_key not in all_instances:
            print("** no instance found **")
            return
        if len(args) < 3:
            print("** attribute name missing **")
            return
        attribute_name = args[2]
        if len(args) < 4:
            print("** value missing **")
            return
        attribute_value = args[3]

        instance = all_instances[instance_key]
        setattr(instance, attribute_name, attribute_value)
        instance.save()

        if len(args) < 3:
            print("** dictionary representation missing **")
            return
        dictionary_repr = ' '.join(args[2:])
        instance = all_instances[instance_key]

        try:
            update_dict = eval(dictionary_repr)
        except Exception as e:
            print(f"Error evaluating dictionary representation: {e}")
            return

        if not isinstance(update_dict, dict):
            print("** invalid dictionary representation **")
            return

        for key, value in update_dict.items():
            setattr(instance, key, value)
        instance.save()

    def do_count(self, user_input):
        """Counts the instances of a class."""
        args = user_input.split()
        if not args:
            print("** class name missing **")
            return

        class_name = args[0]
        if class_name in self.__classes:
            class_object = self.__classes[class_name]
            instances_count = sum(1 for instance in storage.all().values() if isinstance(instance, class_object))
            print(instances_count)
        else:
            print("** class doesn't exist **")


if __name__ == '__main__':
    HBNBCommand().cmdloop()
