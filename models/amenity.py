#!/usr/bin/python3
""" definition of the amenity class"""
from models.base_model import BaseModel


class Amenity(BaseModel):
    """ representation of the Amenity class
    Attributes:
        name: string - amneity name
    """

    name = ""
