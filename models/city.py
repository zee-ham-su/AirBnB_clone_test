#!/usr/bin/python3
""" definition of the City class
"""
from models.base_model import BaseModel


class City(BaseModel):
    """ represents the City class

    Attributes:
    state_id: string - the state id
    name: string - city name

    """

    state_id = ""
    name = ""
