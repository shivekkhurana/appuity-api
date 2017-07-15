from flask_restful import Resource, reqparse

class Reviews(Resource):
    def get(self, app_id):
        return {'msg': 'Showing reviews for {}'.format(app_id)}
        