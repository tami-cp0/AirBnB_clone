#!/usr/bin/python3


import unittest
import os
from datetime import datetime
from unittest.mock import patch
from io import StringIO
from models.base_model import BaseModel
from models.engine.file_storage import FileStorage


class FileStorage(unittest.TestCase):
    def setUp(self):
        # Create new storage instance
        global test_storage
        test_storage = FileStorage()
        # change path so it does not affect my package json file
        test_storage._FileStorage__file_path = "test_file.json"

        global basemodel
        basemodel = BaseModel()

    def tearDown(self):
        # Clean up after each test if needed
        try:
            os.remove("test_file.json")
        except FileNotFoundError:
            pass


if __name__ == '__main__':
    unittest.main()
