#!/usr/bin/python3
"""
Console script for the hbnb command interpreter.
"""


import cmd
from models.base_models import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from models import storage
import json
import re
import shlex


class HBNHCommand(cmd.Cmd):
    # Set the custom prompt
    prompt = "(hbnb) "
    # Dictionary of valid classes
    __valid_classes = {
        "BaseModel": BaseModel,
        "User": User,
        "State": State,
        "City": City,
        "Amenity": Amenity,
        "Place": Place,
        "Review": Review
    }

    def default(self, line):
        """
        Method called on an input line when the command prefix is not recognized.

        Args:
            line (str): The user input line to process.

        This method interprets the user input, extracts class names, commands, and attributes,
        and dispatches the corresponding actions based on predefined rules. It supports commands
        like 'all()', 'count()', 'show()', 'destroy()', and 'update()', handling class instances
        and their attributes accordingly.
        """
        # checks if string needs to be parsed
        match = re.match(r'^\w+\..*\)', line)
        if match:
            # store captured string
            line_data = match.group()
            if line_data.endswith("all()") or line_data.endswith("count()"):
                class_name, command = line_data.strip("()").split(".")
                # list of allowed commands that require no class attributes
                valid_commands = {"all": self.do_all, "count": self.count}

                if command in valid_commands:
                    valid_commands[command](class_name)
            elif line_data.endswith(')'):
                # obtain class name with leftover data
                class_name, class_data = line_data.rstrip(")").split(".")
                # obtain command to execute with leftover class attributes
                command, class_attributes = class_data.split("(")
                # check if a dictionary was provided for do_update
                match_data = re.match(r'(".*")\s*,\s*({.*})', class_attributes)
                if match_data:
                    attribute_1, attribute_2 = match_data.groups()
                    attribute_3 = ""
                else:
                    attributes = class_attributes.split(", ")
                    # assign an empty string if a certain attribute is omitted
                    attribute_1 = attributes[0] if len(attributes) > 0 else ""
                    attribute_2 = attributes[1] if len(attributes) > 1 else ""
                    attribute_3 = attributes[2] if len(attributes) > 2 else ""
                # list of allowed commands that require class attributes
                valid_commands = {
                    "show": self.do_show, "destroy": self.do_destroy,
                    "update": self.do_update
                }
                if command in valid_commands:
                    if command == "update":
                        valid_commands[command](
                            f"{class_name} {attribute_1} "
                            f"{attribute_2} {attribute_3}"
                        )
                    else:
                        valid_commands[command](
                            f"{class_name} {attribute_1} {attribute_2}"
                        )
        else:
            pass

    def count(self, arg):
        """
        counts the number of instances found
        """
        number_of_classes = 0
        obj_dict = storage.all()

        for key in obj_dict:
            name, obj_id = key.split(".")
            if name == arg:
                number_of_classes += 1
        print("{:d}".format(number_of_classes))

    def do_quit(self, line):
        """
        [Description] - Exit the command interpreter.

        [Usage] - quit
        """
        return True

    def do_EOF(self, line):
        """
        [Description] - Exit the command interpreter.

        [Usage] - EOF (Ctrl+D on Unix/Linux, Ctrl+Z on Windows)
        """
        return True

    def emptyline(self):
        """Description - Do nothing on an empty line."""
        pass

    def validate_data(self, class_data):
        """
        supporting function that validates data from cmd line.
        Used within: do_show, do_destroy
        """
        if not class_data:
            print("** class name missing **")
            return False
        # Handles invalid class
        elif class_data[0] not in self.__valid_classes:
            print("** class doesn't exist **")
            return False
        # Handle missing id
        elif len(class_data) < 2:
            print("** instance id missing **")
            return False

        return True

    def do_create(self, line):
        """
        [Description] - Create a new instance of a specified class
                        (derived from BaseModel), save it to the JSON
                        file, and print the id of the created instance.

        Returns:
            ID of the new instance

        [Usage] - create <class_name>
        """
        if not line:
            print("** class name missing **")
        else:
            class_data = line.split()
            # checks if the First argument is a correct class
            if class_data[0] in self.__valid_classes:
                instance = self.__valid_classes[class_data[0]]()
                # saves instance to the file storage
                instance.save()
                print(instance.id)
            else:
                print("** class doesn't exist **")

    def do_show(self, line):
        """
        [Description] - Prints the string representation of an instance
                        based on the class name and id.

        Returns:
            Metadata of the class

        [Usage] - show <class_name> <class_id>
        """
        # Store input in a list
        class_data = shlex.split(line)

        if self.validate_data(class_data):
            # Access the dictionary of stored objects.
            obj_dict = storage.all()
            # Constructs access key
            key = f"{class_data[0]}.{class_data[1]}"
            # Checks if instance exists
            if key in obj_dict:
                print(obj_dict[key])
            else:
                print("** no instance found **")

    def do_destroy(self, line):
        """
        [Description] - Deletes an instance based on the class name and id.

        Returns:
            None

        [Usage] - destroy <class_name> <class_id>
        """
        class_data = shlex.split(line)

        if self.validate_data(class_data):
            # Acess dictionary of stored objects.
            obj_dict = storage.all()
            # Constructs access key.
            key = f"{class_data[0]}.{class_data[1]}"
            # Checks if instance exists.
            if key in obj_dict:
                # Destroys the instance and writes changes to file storage.
                del obj_dict[key]
                storage.save()
            else:
                print("** no instance found **")

    def do_all(self, line):
        """
        [Description] - Print all instances or all instances
                        of a specific class.

        [Usage] - all or all <class_name>
        """
        # Retrieve the dictionary of stored objects.
        obj_dict = storage.all()
        # Checks if an argument is passed.
        if not line:
            obj_list = [f"{k}: {v}" for k, v in obj_dict.items()]
            print(obj_list)
        else:
            class_data = line.split()
            # Check if first argument is a valid class.
            if class_data[0] not in self.__valid_classes:
                print("** class doesn't exist **")
            else:
                # Only includes keys that starts with the specified class name
                obj_list = [
                    f"{k}: {v}"
                    for k, v in obj_dict.items() if k.startswith(class_data[0])
                ]
                print(obj_list)

    def do_update(self, line):
        """
        [Description] - Update attributes of an instance based on the class
                        name and id. This method parses the user input,
                        validates the data, and updates the attributes of
                        an instance stored in the dictionary of stored objects.

        Returns:
            None

        [Usage] - update <class_name> <class_id>
                  <attribute_name> <attribute_value>
        """
        # checks if a dictionary representation of attributes was provided
        match_data = re.match(r'^(\w+)\s+(.*)\s+({.+}).*', line)
        if match_data:
            # Initializes the class_data list with the first group
            class_data = [match_data.group(1)]
            #  use shlex to consider quotes and whitespace.
            class_data.extend(shlex.split(match_data.group(2)))
            # converts the string to a python object for use and append.
            class_data.append(
                json.loads(match_data.group(3).replace("'", "\""))
            )
        else:
            class_data = shlex.split(line)

        if self.validate_data(class_data):
            # Access the dictionary of stored objects in file storage.
            obj_dict = storage.all()
            # Constructs access key
            key = f"{class_data[0]}.{class_data[1]}"

            # Checks if instance exists
            if key in obj_dict:
                if len(class_data) == 2:
                    print("** attribute name missing **")
                    return

                if isinstance(class_data[2], dict) and len(class_data) == 3:
                    if class_data[2]:
                        for k, v in class_data[2].items():
                            if k:
                                if v:
                                    # Update the attribute with the new value
                                    setattr(obj_dict[key], k, v)
                                else:
                                    print("** value missing **")
                            else:
                                print("** attribute name missing **")
                    else:
                        print("** attribute name missing **")

                    # write changes to storage
                    obj_dict[key].save()
                    return

                if len(class_data) == 3:
                    print("** value missing **")
                else:
                    # Update the attribute with the new value
                    setattr(obj_dict[key], class_data[2], class_data[3])
                    # write changes to storage
                    obj_dict[key].save()
            else:
                print("** no instance found **")


if __name__ == "__main__":
    HBNHCommand().cmdloop()
