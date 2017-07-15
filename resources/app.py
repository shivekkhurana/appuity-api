from flask_restful import Resource, reqparse

# List resource
class Apps(Resource):
	def get(self):
		return {'msg': 'All apps'}


# Instance resource
class App(Resource):
	def get(self, app_id):
		return {
			'msg': 'Data for {}'.format(app_id)
		}