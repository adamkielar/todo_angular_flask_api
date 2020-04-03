import datetime

from peewee import *

import config

DATABASE = 'todos.db'

database = SqliteDatabase(DATABASE)


class Todo(Model):
    name = CharField(max_length=250)
    created_at = DateTimeField(default=datetime.datetime.now)
    completed = BooleanField(default=False)
    edited = BooleanField(default=False)

    class Meta:
        database = database

def initialize():
    with database:
        database.drop_tables([Todo], safe=True)
        database.create_tables([Todo], safe=True)
