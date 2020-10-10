import datetime

from argon2 import PasswordHasher
from peewee import *

import config

DATABASE = SqliteDatabase('books.db')
HASHER = PasswordHasher()


class User(Model):
    username = CharField(unique=True)
    password = CharField()
    
    class Meta:
        database = DATABASE
        
    @classmethod
    def create_user(cls, username, password, **kwargs):
        try:
            cls.get(cls.username**username)
        except cls.DoesNotExist:
            user = cls(username=username)
            user.password = user.hash_password(password)
            user.save()
            return user
        else:
            raise Exception("User already exists.")
            
    @staticmethod
    def hash_password(password):
        return HASHER.hash(password)
    
    def verify_password(self, password):
        return HASHER.verify(self.password, password)


class Book(Model):
    title = CharField()
    author = CharField()
    created_at = DateTimeField(default=datetime.datetime.now)
    
    class Meta:
        database = DATABASE


def initialize():
    DATABASE.connect()
    DATABASE.create_tables([User, Book], safe=True)
    DATABASE.close()