from flask_restful import Resource

class ReviewsResource(Resource):
    def get(self, play_store_id):
        return {'msg': 'Showing reviews for {}'.format(play_store_id)}
        