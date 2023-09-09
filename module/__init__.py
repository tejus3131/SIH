
# In-built Module Import

from flask import Flask
from flask_restful import Api
from flask_cors import CORS

# Custom Module Import

from .routes import Routes

from .services.authentication import AuthenticationManager
from .services.database import DatabaseManager

class Server:

    _instance = None

    URI = 'mongodb+srv://tejusgupta:tZvn1Apfs423uXnA@cluster0.ovujbs6.mongodb.net/?retryWrites=true&w=majority'

    def __new__(cls, namespace):
        if cls._instance is None:
            cls._instance = super(Server, cls).__new__(cls)
            cls._instance.initialise_server(namespace)
            Routes.add_routes(cls._instance.app, cls._instance.api)
        return cls._instance

    def initialise_server(self, namespace):
        self.app = Flask(namespace)
        self.api = Api(self.app)
        CORS(self.app)
        self.app.config['SECRET_KEY'] = "ModuleBasedServer"

        DatabaseManager(self.URI)



    def run(self, host='127.0.0.1', port=80, debug=False):
        self.app.run(host=host, port=port, debug=debug)
