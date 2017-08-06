from flask import Flask
from flask_restful import Resource, Api

from resources import App, Apps, Index, Reviews, Authors

app = Flask(__name__)
api = Api(app)

api.add_resource(Index, '/')
api.add_resource(Authors, '/authors')
api.add_resource(Apps, '/apps')
api.add_resource(App, '/apps/<play_store_id>')
api.add_resource(Reviews, '/apps/<play_store_id>/reviews')
# api.add_resource(Reviews, '/apps/<play_store_id>/authors')
# api.add_resource(User, '/users')

if __name__ == '__main__':
    app.run(debug=True)