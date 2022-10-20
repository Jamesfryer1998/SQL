from flask import Flask, request
from flask_restful import Resource, Api
from SQL_connect import *

class SymbolLoader(Resource):
    def get(self, id):
        SQL = SQLConnect(id, 'localhost', 'postgres', 'mysecretpassword')
        SQL.create_table()
        SQL.execute_values()
        SQL.check_tables()
        SQL.update_table()

        return {'symbol': id, 'result': 'OK'}

if __name__ == '__main__':
    app = Flask(__name__)
    api = Api(app)
    api.add_resource(SymbolLoader, '/load/<string:id>')
    app.run(debug=True)