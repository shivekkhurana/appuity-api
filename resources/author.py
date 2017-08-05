from flask_restful import Resource

from models import Author
from utils import Response

# List resource
class AuthorsResource(Resource):
	def get(self):
		return Response.collection('Authors list', Author.all())
