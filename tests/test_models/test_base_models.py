#!/usr/python3
"""
test module for BaseModel
"""


import unittest
import os
from unittest.mock import patch
from datetime import datetime
from io import StringIO
from models.base_model import BaseModel
from models.engine.file_storage import FileStorage


class TestBaseModel(unittest.TestCase):
    """
    """
    def setUp(self):
        # Create new storage instance
        global test_storage
        test_storage = FileStorage()
        # change path so it does not affect my package json file
        FileStorage._FileStorage__file_path = "test_file.json"
        # set up instance for testing
        global basemodel
        basemodel = BaseModel()
        

    def tearDown(self):
        # Clean up after each test if needed
        try:
            os.remove("test_file.json")
        except FileNotFoundError:
            pass

    def test_init(self):
        """Test initialization of a BaseModel instance with no
        arguments passed
        """
        # check if id is a str
        self.assertIsInstance(basemodel.id, str)
        # check updated_at and created_at are datetime obj
        self.assertIsInstance(basemodel.updated_at, datetime)
        self.assertIsInstance(basemodel.created_at, datetime)
        # check if base_model is an instance of BaseModel
        self.assertIsInstance(basemodel, BaseModel)
        # check if base_model is a valid object __class__
        self.assertTrue(hasattr(basemodel, "__class__"))
        # check if calling new() was successful
        self.assertIn(basemodel, test_storage.all().values())

    def test_str(self):
        """Testing string representation of BaseModel class"""
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            print(basemodel)

            # Access the printed output from mock_stdout.getvalue()
            printed_output = mock_stdout.getvalue()

            self.assertEqual(
                f"[{basemodel.__class__.__name__}] ({basemodel.id}) "
                f"<{basemodel.__dict__}>\n",
                printed_output
            )

    def test_save(self):
        """Testing save method of BaseModel class"""
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            basemodel.save()
            print(basemodel.updated_at.strftime('%Y-%m-%dT%H:%M:%S'))

            printed_output = mock_stdout.getvalue()

            self.assertEqual(
                f"{datetime.now().strftime('%Y-%m-%dT%H:%M:%S')}\n",
                printed_output
            )

    def test_to_dict(self):
        """Testing to_dict method of BaseModel class"""
        dict_example = {
            "id": f"{basemodel.id}",
            "created_at": f"{basemodel.created_at.isoformat()}",
            "updated_at": f"{basemodel.updated_at.isoformat()}",
            "__class__": f"{basemodel.__class__.__name__}"
        }

        self.assertDictEqual(basemodel.to_dict(), dict_example)

    def test_with_kwargs(self):
        """Test initialization of BaseModel with kwargs"""
        dict_example = {
            "id": "78792ec6-ed2c-4ce8-9300-bb060e6ef00b",
            "created_at": f"{datetime.now().isoformat()}",
            "updated_at": f"{datetime.now().isoformat()}",
            "__class__": "BaseModel",
            "state": "Oyo"
        }

        basemodel2 = BaseModel(**dict_example)
        self.assertEqual(dict_example["state"], basemodel2.state)
        self.assertDictEqual(basemodel2.to_dict(), dict_example)


if __name__ == '__main__':
    unittest.main()
