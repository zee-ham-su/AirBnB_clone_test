#!/usr/bin/python3
""" a state class that inherit from BaseModel
"""
from models.base_model import BaseModel


class State(BaseModel):
    """ this represents State class

    Attributes:
        name: string - the state's name
    """
    name = ""
