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
    "completed": fields.Boolean,
    "edited": fields.Boolean,
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
        self.reqparse.add_argument(
            "completed", 
            type=inputs.boolean, 
            location=["form", "json"],
        )
        super().__init__()


    def get(self):
        return [marshal(todo, todo_fields) for todo in models.Todo.select()], 200


    @marshal_with(todo_fields)
    def post(self):
        args = self.reqparse.parse_args()
        todo = models.Todo.create(**args)
        return (todo, 201, {'Location': url_for('resources.todos.todo', id=todo.id)})


todos_api = Blueprint("resources.todos", __name__)
api = Api(todos_api)
api.add_resource(TodoList, "/todos", endpoint="todos")
api.add_resource(TodoList, "/todos/<int:id>", endpoint="todo")
