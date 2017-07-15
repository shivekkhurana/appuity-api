from flask_restful import Resource

class Index(Resource):
    def get(self):
        return {'msg': 'Appuity api up and running.'}