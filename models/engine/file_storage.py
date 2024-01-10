#!/usr/bin/python3
"""
Module containing the FileStorage class.

This module defines a simple file-based storage mechanism using JSON.
The FileStorage class handles the serialization and deserialization
of Python objects to and from a JSON file.

Classes:
    - FileStorage: Handles storage, retrieval,
    and persistence of objects to a JSON file.
"""


import json
import os
from models.base_models import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class FileStorage:
    """
    FileStorage class for handling storage, retrieval,
    and persistence of objects.

    Attributes:
        __file_path (str): The path to the JSON file for storing objects.
        __objects (dict): A dictionary to store objects,
        indexed by their unique identifier.

    Methods:
        - all(self): Returns the dictionary __objects.
        - new(self, obj): Adds a new object to the dictionary __objects.
        - save(self): Serializes __objects to JSON and writes it to the file.
        - reload(self): Deserializes JSON from the file and updates __objects.
    """
    __file_path = "file.json"
    __objects = {}
    # Dictionary of valid classes
    __valid_class = {
        "BaseModel": BaseModel,
        "User": User,
        "State": State,
        "City": City,
        "Amenity": Amenity,
        "Place": Place,
        "Review": Review
    }

    def all(self):
        """Returns the dictionary __objects."""
        return self.__objects

    def new(self, obj):
        """
        Adds a new object to the dictionary __objects.

        Args:
            obj: The object to be added.
        """
        # store instances in the __object dict
        # The value is the memory address of the instance
        self.__objects[f"{obj.__class__.__name__}.{obj.id}"] = obj

    def save(self):
        """
        Serializes __objects to JSON and writes it to the file.
        """
        obj_dict_copy = {}
        for key, obj in self.__objects.items():
            # Retrieves instance to obtain the __dict__ representation
            obj_dict_copy[key] = obj.to_dict()
        with open(self.__file_path, "w", encoding="utf-8") as json_file:
            # stores key and value in a json file
            json.dump(obj_dict_copy, json_file)

    def reload(self):
        """
        Deserializes JSON from the file and updates __objects.
        """
        # Checks if file exists
        if os.path.exists(self.__file_path):
            with open(self.__file_path, "r", encoding="utf-8") as json_file:
                # Deserializes the file into a dictionary
                obj_dict = json.load(json_file)
                for key, value in obj_dict.items():
                    class_name, class_id = key.split(".")
                    # globals() allows dynamic access to variables
                    # based on their names as strings.
                    self.__objects[key] = self.__valid_class[class_name](**value)
