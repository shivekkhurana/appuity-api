from flask_restful import Resource, reqparse

from models import Author
from utils import Response

# List resource
class AuthorsResource(Resource):
    def get(self):
        args = reqparse.RequestParser().add_argument('page_num', type=int, required=False).parse_args()
        return Response.pagination(
            'Authors delivered',
            Author,
            args.get('page_num') or 1,
            8
        )
