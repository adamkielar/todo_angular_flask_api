import sys
sys.path.append("/Volumes/imac2/todo_angular_flask_api")
import unittest
import todo_app

from peewee import *

from models import Todo

test_db = SqliteDatabase(':memory:')

class TestDatabase(unittest.TestCase):
    database = test_db

    def test_connection(self):
        conn = self.database.connection()
        self.assertFalse(self.database.is_closed())
        self.database.close()
        self.assertTrue(self.database.is_closed())
        conn = self.database.connection()
        self.assertFalse(self.database.is_closed())
        self.database.close()

class TodoModelTestCase(unittest.TestCase):
    def setUp(self):
        test_db.bind([Todo])
        test_db.connect()
        test_db.create_tables([Todo], safe=True)

    def tearDown(self):
        test_db.drop_tables([Todo])
        test_db.close()

    def test_todo_creation(self):
        Todo.create(
            name='run today',
        )

        self.assertEqual(Todo.select().count(), 1)

class ViewTestCase(unittest.TestCase):
    def setUp(self):
        todo_app.app.testing = True
        self.app = todo_app.app.test_client()
        test_db.bind([Todo])
        test_db.connect()
        test_db.create_tables([Todo], safe=True)

    def tearDown(self):
        test_db.drop_tables([Todo])
        test_db.close()

class AppViewsTestCase(ViewTestCase):
    def test_my_todos_view(self):
        rv = self.app.get("/")
        self.assertIn("todolistapp", rv.get_data(as_text=True).lower())



if __name__ == '__main__':
    unittest.main()