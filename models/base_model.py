#!/usr/bin/python3
"""
BaseModel class definition
"""
from datetime import datetime
import models
from uuid import uuid4


class BaseModel:
    """ BaseModel class of the HBnB project"""

    def __init__(self, *args, **kwargs):
        """
        Initializes a new instance of the BaseModel class.

        Args:
            *args: Not used.
            **kwargs: Dictionary containing attribute values
        for initialization.

        """

        self.id = str(uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

        if kwargs:
            for k, v in kwargs.items():
                if k != '__class__':
                    if k in ['created_at', 'updated_at']:
                        self.__dict__[k] = datetime.strptime(
                            v, '%Y-%m-%dT%H:%M:%S.%f')
                    else:
                        self.__dict__[k] = v
        else:
            models.storage.new(self)

    def save(self):
        """
         Updates the 'updated_at' attribute with the current
         timestamp.
        """
        self.updated_at = datetime.now()
        models.storage.save()

    def to_dict(self):
        """
        Converts the instance attributes to a dictionary.

        Returns:
            dict: A dictionary containing class name,
        attributes,
        and timestamps.
        """
        cstm_dict = self.__dict__.copy()
        cstm_dict['__class__'] = self.__class__.__name__
        cstm_dict['created_at'] = self.created_at.isoformat()
        cstm_dict['updated_at'] = self.updated_at.isoformat()
        return cstm_dict

    def __str__(self):
        """
        Returns a string representation of the instance.

        Returns:
            str: A string containing class name, instance id,
        and attribute dictionary.
        """
        return "[{}] ({}) {}".format(self.__class__.__name__,
                                     self.id, self.__dict__)
