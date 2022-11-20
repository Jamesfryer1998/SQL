from flask import Flask, request
from flask_restful import Resource, Api
from SQL_connect import *

class SymbolLoader(Resource):
    def get(self, id):
        crypto_cache = '/Users/james/Projects/SQL/Cache/crypto_data'
        SQL = SQLConnect(id, crypto_cache, 'localhost', 'postgres', 'mysecretpassword')
        SQL.load_data()
        
        return {'symbol': id, 'result': 'OK'}

if __name__ == '__main__':
    app = Flask(__name__)
    api = Api(app)
    api.add_resource(SymbolLoader, '/load/<string:id>')
    app.run(debug=True)
    # app.run(host='127.0.0.1')
    app.run(host='0.0.0.0')