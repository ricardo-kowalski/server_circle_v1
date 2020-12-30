from calculator import distance

from flask import Flask
from flask_restful import reqparse, abort, Api, Resource, request

app = Flask(__name__)
api = Api(app)


# d = distance((25.2285, 55.3273), (26.2285, 54.3273))
# print(d)


# LOCATIONS = {
#     'location1': {'id': 1, 'location': [25.2285, 55.3273]},
#     'location2': {'id': 2, 'location': [26.2285, 54.3273]},
# }
LOCATIONS = {
    'distance': {'location1': [25.2285, 55.3273], 'location2': [26.2285, 54.3273]},
}


def abort_if_todo_doesnt_exist(todo_id):
    if todo_id not in LOCATIONS:
        abort(404, message="Todo {} doesn't exist".format(todo_id))


parser = reqparse.RequestParser()
parser.add_argument('location')


# Todo
# shows a single todo item and lets you delete a todo item
class Todo(Resource):
    def get(self, todo_id):
        abort_if_todo_doesnt_exist(todo_id)
        return LOCATIONS[todo_id]
        # return distance((25.2285, 55.3273), (26.2285, 54.3273))

    def delete(self, todo_id):
        abort_if_todo_doesnt_exist(todo_id)
        del LOCATIONS[todo_id]
        return '', 204

    def put(self, todo_id):
        args = parser.parse_args()
        task = {'location': args['location']}
        LOCATIONS[todo_id] = task
        return task, 201


# TodoList
# shows a list of all todos, and lets you POST to add new tasks
class TodoList(Resource):
    def get(self):
        # return LOCATIONS
        return distance((25.2285, 55.3273), (26.2285, 54.3273))

    def post(self):
        # args = parser.parse_args()
        # todo_id = int(max(TODOS.keys()).lstrip('todo')) + 1
        # todo_id = 'todo%i' % todo_id
        # TODOS[todo_id] = {'task': args['task']}
        # return TODOS[todo_id], 201

        json_data = request.get_json(force=True)
        id = json_data['id']
        lc = json_data['location']

        # return jsonify(u=un, p=pw)

        todo_id = int(max(LOCATIONS.keys()).lstrip('location')) + 1
        todo_id = 'todo%i' % todo_id
        LOCATIONS[todo_id] = {'location': lc}
        return LOCATIONS[todo_id], 201


##
# Actually setup the Api resource routing here
##
api.add_resource(TodoList, '/todos')
api.add_resource(Todo, '/todos/<todo_id>')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
