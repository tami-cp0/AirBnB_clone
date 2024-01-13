#!/usr/bin/python3
"""
BaseModel module - Defines the BaseModel class for the AirBnB_clone project.

This module contains the BaseModel class,
which serves as the base class for all
other classes in the project. It includes methods for initialization, string
representation, saving to storage, and converting to a dictionary.
"""


import uuid
from datetime import datetime
import models


class BaseModel:
    """
    BaseModel class - Base class for AirBnB_clone.

    Attributes:
        id (str): Unique identifier.
        created_at (datetime): Date and time of creation.
        updated_at (datetime): Date and time of last update.

    Methods:
        __init__: Initializes a new instance.
        __str__: Overrides string representation.
        save: Updates 'updated_at' and saves to storage.
        to_dict: Converts to a dictionary for serialization.
    """
    # created just for unit testing
    __time_format = '%Y-%m-%dT%H:%M:%S.%f'

    def __init__(self, *args, **kwargs):
        """
        Initializes a new instance of the BaseModel class.

        Args:
            args: Variable-length argument list (unused).
            kwargs: Keyword arguments for initialization.

        If kwargs is not empty, attributes are loaded from kwargs. Otherwise,
        new attributes are generated, and the instance is added to storage.
        """
        if kwargs:
            for key, value in kwargs.items():
                if key == "__class__":
                    continue
                elif key in ['created_at', 'updated_at']:
                    setattr(
                        self, key, datetime.strptime(
                            value, self.__time_format
                            )
                    )
                    continue
                else:
                    setattr(self, key, value)
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
            models.storage.new(self)

    def __str__(self):
        """
        Override the string representation of the BaseModel.
        Returns:
            str: A formatted string representation of the BaseModel.
        """
        return "[{}] ({}) {}".format(self.__class__.__name__,
                                     self.id, self.__dict__)

    def save(self):
        """
        Updates the public instance attribute updated_at
        with the current datetime
        and saves the instance to storage.
        """
        self.updated_at = datetime.now()
        models.storage.save()

    def to_dict(self):
        """
        Converts the instance to a dictionary containing
        all keys/values of __dict__.

        Returns:
            dict: A dictionary representation of the BaseModel instance.
        """
        obj_dict = self.__dict__.copy()

        # Add or modify specific attributes in the dictionary
        obj_dict['__class__'] = self.__class__.__name__

        # Convert created_at and updated_at to ISO format strings
        obj_dict['created_at'] = self.created_at.isoformat()
        obj_dict['updated_at'] = self.updated_at.isoformat()

        return obj_dict
