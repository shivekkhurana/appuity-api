from flask_restful import Resource
from models import Author

# List resource
class Authors(Resource):
	def get(self):
		authors = Author.all()
		return {'msg': 'Authors list', 'authors': authors.serialize()}

