import unittest
import json
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
        try:
            with open('mock/todos.json') as data:
                todo_data = json.load(data)
                for todo in todo_data:
                    Todo.create(**todo)
        except DatabaseError:
            print("Sample data not loaded")
            pass

    def tearDown(self):
        test_db.drop_tables([Todo])
        test_db.close()


class AppViewsTestCase(ViewTestCase):
    def test_my_todos_view(self):
        response = self.app.get("/")
        self.assertIn("My TODOs!", response.get_data(as_text=True))


class ApiTestCase(ViewTestCase):
    def test_get_todo_list(self):
        response = self.app.get("/api/v1/todos")
        self.assertEqual(response.status_code, 200)
        
    def test_post_todo_list(self):
        todo = json.dumps({
            "name": "run 5km",
            "completed": "false",
            "edited": "true",
        })
        response = self.app.post("/api/v1/todos", data=todo, headers={"Content-Type": "application/json"})
        self.assertEqual(response.status_code, 201)


if __name__ == '__main__':
    unittest.main()
