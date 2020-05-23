__version__ = '0.0.1'
from flask import Flask, render_template, request, jsonify
from flask_restful import Api, Resource

class Store(object):
    '''
    Interface for storing and updating each person's attributes.
    '''
    def __init__(self, names=[]):
        self.default = False
        self.names = names
        self.state = {
            name: dict(
                name=name,
                doNotDisturb=self.default,
            )
            for name in names
        }

    def get_state(self):
        print(self.state)
        return self.state

    def toggle_status(self, name):
        oldStatus = self.state[name]['doNotDisturb']
        newStatus = not oldStatus
        print(f'{name}: {oldStatus} -> {newStatus}')
        self.state[name]['doNotDisturb'] = newStatus
        return True


settings = dict(
    APP_VERSION=__version__,
    STORE=Store(names=['Chris', 'Leigh', 'Michael', 'Sarah']),
)

app = Flask(__name__)
app.config.update(settings)
api = Api(app)

@app.route('/')
def index():
    return render_template('index.html')

class ApiResource(Resource):
    '''
    Each user can have a `doNotDisturb` as True or False
    True is RED, False is BLUE

    GET     ->  Returns the current data store
    POST    ->  Toggles the status of specified user
                /api?name=<name>
    '''
    @staticmethod
    def get_state():
        state = app.config['STORE'].get_state()
        return jsonify(state)

    @staticmethod
    def toggle_status(name):
        store = app.config['STORE']
        return store.toggle_status(name)

    def get(self):
        return self.get_state()

    def post(self):
        name = request.args.get('name')
        self.toggle_status(name)
        return self.get_state()

api.add_resource(ApiResource, '/api')
