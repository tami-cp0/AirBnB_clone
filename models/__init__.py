"""
AirBnB_clone package initialization

This package, "AirBnB_clone," serves as an implementation of an AirBnB clone,
with components for handling storage, retrieval, and persistence of objects.

Modules:
- engine.file_storage: Provides a FileStorage class for handling storage.

Author: Oluwatamilore Olugbesan
email: findtamilore@gmail.com

Usage:
Import the package and its modules using:
    from AirBnB_clone import engine

Version: 1.0
"""


from models.engine.file_storage import FileStorage


__author__ = 'Oluwatamilore Olugbesan'

# The list of modules to load
__all__ = ["base_models"]

# Create a unique FileStorage instance for the  application
storage = FileStorage()

# load data from the file (if the file exists)
storage.reload()
