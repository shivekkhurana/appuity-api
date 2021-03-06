from flask import Flask
from flask_restful import Resource, Api
from flask_cors import CORS
from utils import ow_invoke

from resources import App, Apps, Index, Reviews, Authors

app = Flask(__name__)
CORS(app)

api = Api(app)
api.add_resource(Index, '/')
api.add_resource(Authors, '/authors')
api.add_resource(Apps, '/apps')
api.add_resource(App, '/apps/<play_store_id>')
api.add_resource(Reviews, '/apps/<play_store_id>/reviews')
# api.add_resource(Reviews, '/apps/<play_store_id>/authors')
# api.add_resource(User, '/users')

def openwhisk_handler(args):
	return ow_invoke(app, args)

if __name__ == '__main__':
    app.run(debug=True)