#!/usr/bin/python3
"""This module defines a class to manage file storage for hbnb clone"""
from models.base_model import BaseModel
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review
import json
from json.decoder import JSONDecodeError


class FileStorage:
    """This class manages storage of hbnb models in JSON format"""
    __file_path = 'file.json'
    __objects = {}

    def all(self, cls=None):
        """Returns a dictionary of models currently in storage"""
        if cls is None or FileStorage.__objects is None:
            return FileStorage.__objects
        else:
            returned_dic = {}
            for key, value in FileStorage.__objects.items():
                if key.partition('.')[0] == cls.__name__:
                    returned_dic[key] = value
            return returned_dic

    def new(self, obj):
        """Adds new object to storage dictionary"""
        self.all().update({obj.to_dict()['__class__'] + '.' + obj.id: obj})

    def save(self):
        """Saves storage dictionary to file"""
        with open(FileStorage.__file_path, 'w') as f:
            temp = {}
            temp.update(FileStorage.__objects)
            for key, val in temp.items():
                temp[key] = val.to_dict()
            json.dump(temp, f)

    def delete(self, obj=None):
        """delete an object"""
        if obj is not None:
            class_obj_ref = type(obj).__name__ + '.' + obj.id
            if class_obj_ref in FileStorage.__objects.keys():
                del self.__objects[class_obj_ref]
        else:
            return

    def reload(self):
        """Loads storage dictionary from file"""
        classes = {
                    'BaseModel': BaseModel, 'User': User, 'Place': Place,
                    'State': State, 'City': City, 'Amenity': Amenity,
                    'Review': Review
                  }
        try:
            temp = {}
            with open(FileStorage.__file_path, 'r') as f:
                    temp = json.load(f)
                    for key, val in temp.items():
                        self.all()[key] = classes[val['__class__']](**val)

        except FileNotFoundError:
            pass

    def empty(self):
        """Empyts both the runtime and the file storage"""

        del FileStorage.__objects
        FileStorage.__objects = {}
        self.save()
