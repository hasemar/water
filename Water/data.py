'''
Data Module:

This module handles the sqlite interactions for the other modules when pulling or entering data into the package database 
'''

import sqlite3
from contextlib import closing
from os import path

BASE_DIR = path.dirname(path.abspath(__file__))
db_path = path.join(BASE_DIR, "water.db")

class data:
    '''defines database interaction object

         :param object_class: class that is interacting with database
         :type object_class: string 
    '''

    def __init__(self, object_class):
        self.object_class = object_class

if __name__=="__main__":
    print("test script:")