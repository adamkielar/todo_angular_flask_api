import json
from flask import Flask, render_template
from flask_cors import CORS

import config
import models
from resources.todos import todos_api


app = Flask(__name__)
CORS(app)
app.register_blueprint(todos_api, url_prefix="/api/v1")


@app.route("/")
def my_todos():
    return render_template("index.html")


if __name__ == "__main__":
    models.initialize()
    try:
        with open('mock/todos.json') as data:
            todo_data = json.load(data)
            for todo in todo_data:
                models.Todo.create(**todo)
    except models.IntegrityError:
        pass
    app.run(debug=config.DEBUG, host=config.HOST, port=config.PORT)
