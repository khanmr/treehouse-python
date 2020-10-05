#
'''Tacocat Models'''
import datetime

from flask.ext.login import UserMixin
from flask.ext.bcrypt import generate_password_hash  # , check_password_hash

# from peewee import *
from peewee import SqliteDatabase, Model
from peewee import (CharField, DateTimeField, BooleanField, TextField,
                    ForeignKeyField)
from peewee import IntegrityError

DATABASE = SqliteDatabase('social.db')


class User(UserMixin, Model):
    """User Model
    """
    email = CharField(unique=True)
    password = CharField(max_length=100)
    joined_at = DateTimeField(default=datetime.datetime.now)
    is_admin = BooleanField(default=False)

    class Meta:
        database = DATABASE

    @classmethod
    def create_user(cls, email, password, admin=False):
        try:
            with DATABASE.transaction():
                cls.create(
                    email=email,
                    password=generate_password_hash(password),
                    is_admin=admin)
        except IntegrityError:
            raise ValueError("User already exists")

        # joined_at
        pass


class Taco(Model):
    """Taco Model
    """
    user = ForeignKeyField(
        rel_model=User,
        related_name='posts'
        )
    protein = CharField()
    shell = CharField()
    cheese = BooleanField(default=False)
    extras = TextField()

    class Meta:
        database = DATABASE


def initialize():
    DATABASE.connect()
    DATABASE.create_tables([User, Taco], safe=True)
    DATABASE.close()
