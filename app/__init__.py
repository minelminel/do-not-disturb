__version__ = '0.0.2'
from flask import Flask, render_template, request, jsonify
from flask_restful import Api, Resource
from flask_redis import FlaskRedis

INDIVIDUALS = ['Chris', 'Leigh', 'Michael', 'Sarah']

class Store(object):
    def __init__(self, app, names=[]):
        self.default = False
        self.expire_seconds = app.config.get('REDIS_EXPIRE_KEY_AFTER_SECONDS')
        self.redis_client = FlaskRedis(app)
        self.names = app.config.get('INDIVIDUALS', [])
        self.init_state()

    def set_status(self, name, status):
        print(f'[Store.set_status] {name} : {status}')
        return self.redis_client.set(name, int(status))

    def get_status(self, name):
        status = self.redis_client.get(name)
        status = bool(int(status.decode('utf-8')))
        print(f'[Store.get_status] {name} : {status}')
        return status

    def init_state(self):
        self.redis_client.flushall()
        for name in self.names:
            print(f'[Store.init_state] {name} : {self.default}')
            self.set_status(name, self.default)

    def state(self):
        state = {}
        for name in self.names:
            state.update(
                {name: dict(
                    name=name, doNotDisturb=self.get_status(name)
                )}
            )
        print(f'[Store.state] {state}')
        return state

    def toggle_status(self, name):
        oldStatus = self.get_status(name)
        newStatus = not oldStatus
        self.set_status(name, newStatus)
        print(f'[Store.toggle_status] {name}: {oldStatus} -> {newStatus}')


settings = dict(
    APP_VERSION=__version__,
    INDIVIDUALS=INDIVIDUALS,
    REDIS_URL='redis://:@redis:6379/0',
    REDIS_EXPIRE_KEY_AFTER_SECONDS=3,
)

app = Flask(__name__)
app.config.update(settings)
api = Api(app)
store = Store(app)

@app.route('/')
def index():
    return render_template('index.html', version=__version__)

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
        return jsonify(store.state())

    def get(self):
        return self.get_state()

    def post(self):
        name = request.args.get('name')
        if name:
            store.toggle_status(name)
        return self.get_state()


api.add_resource(ApiResource, '/api')
