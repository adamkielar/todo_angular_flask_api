import datetime

from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer,
                          BadSignature, SignatureExpired)
from peewee import *

import config

DATABASE = 'todos.db'

database = SqliteDatabase(DATABASE)


class Todo(Model):
    name = CharField(max_length=250)
    url = CharField(unique=True)
    created_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = database

def initialize():
    with database:
        database.create_tables([Todo], safe=True)
