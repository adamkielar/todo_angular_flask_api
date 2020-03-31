from flask import jsonify, Blueprint, abort

from flask_restful import (
    Resource,
    Api,
    reqparse,
    inputs,
    fields,
    marshal,
    marshal_with,
    url_for,
)

import models

todo_fields = {
    "id": fields.Integer,
    "name": fields.String,
    "uri": fields.Url,
    "created_at": fields.DateTime,
}


class TodoList(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            "name",
            required=True,
            help="No todo name provided",
            location=["form", "json"],
        )
        super().__init__()

    @marshal_with(todo_fields)
    def get(self):
        todos = [todo for todo in models.Todo.select()]
        return {"todos": todos}

    @marshal_with(todo_fields)
    def post(self):
        args = self.reqparse.parse_args()
        todo = models.Todo.create(**args)
        return (201, {'Location': url_for('resources.todos.todo', id=todo.id)})

todos_api = Blueprint("resources.todos", __name__)
api = Api(todos_api)
api.add_resource(TodoList, "/todos", endpoint="todos")
