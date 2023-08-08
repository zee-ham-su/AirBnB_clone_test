#!/usr/bin/python3
"""
a class User that inherits from BaseModel
"""
from models.base_model import BaseModel


class User(BaseModel):
    """ class that represents the user
    Attributes:
        email: string - email of the user
        password: string - user's password
        first_name: string - user's first name
        last_name: string -  users's last name
    """

    email = ""
    password = ""
    first_name = ""
    last_name = ""
