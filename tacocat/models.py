import datetime

from argon2 import PasswordHasher
from flask_login import UserMixin
from peewee import *

DATABASE = SqliteDatabase('taco.db')
HASHER = PasswordHasher()

class User(UserMixin, Model):
    username = CharField(unique=True)
    password = CharField(max_length=100)
    joined_at = DateTimeField(default=datetime.datetime.now)
    is_admin = BooleanField(default=False)
    
    class Meta:
        database = DATABASE
        
    @classmethod
    def create_user(cls, username, password, admin=False):
        try:
            with DATABASE.transaction():
                cls.create(
                  username=username,
                  password=HASHER.hash(password),
                  is_admin=admin)
        except IntegrityError:
            raise ValueError("User already exists")

    def verify_password(self, password):
        return HASHER.verify(self.password, password)

class Taco(Model):
    user = ForeignKeyField(
        model=User,
        backref='posts'
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