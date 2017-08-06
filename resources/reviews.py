from flask_restful import Resource, reqparse
import requests
import time

from models import App, Review
from utils import Response

class ReviewsResource(Resource):
    def get(self, play_store_id):
        start_time = time.time()
        app = App.for_play_store_id(play_store_id).first()
        if not app:
            try:
                res = requests.get('https://play.google.com/store/apps/details?id={}'.format(play_store_id))
                if (res.status_code != 200):
                    return Response.error('No app found for app id {}'.format(play_store_id), 404)
            except requests.exceptions.ConnectionError:
                return Response.error('Unable to fetch app from playstore, please try again after sometime', 500)
            
            app = App()
            app.parse_html_and_save(res.text, play_store_id)

        if not app.reviews.count() > 0:
            app.parse_and_save_reviews()

        args = reqparse.RequestParser().add_argument('page_num', type=int, required=False).parse_args()
        return Response.pagination(
            'Reviews Delivered in {} seconds'.format(round(time.time() - start_time, 2)),
            Review.for_play_store_id(play_store_id).with_author(),
            args.get('page_num') or 1,
            8
        )


        
