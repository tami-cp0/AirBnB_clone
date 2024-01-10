#!/usr/bin/python3
"""
Module containing the definition of the User class.
"""


from .base_models import BaseModel


class User(BaseModel):
    """
    User class, a subclass of BaseModel, representing user information.

    Attributes:
        email (str): Email address of the user.
        password (str): Password associated with the user.
        first_name (str): First name of the user.
        last_name (str): Last name of the user.

    Inherits:
        BaseModel: Base class providing common attributes and methods.
    """
    email = ""
    password = ""
    first_name = ""
    last_name = ""
