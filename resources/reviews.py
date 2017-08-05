from flask_restful import Resource
import requests

from models import App, Review
from utils import Response

class ReviewsResource(Resource):
    def get(self, play_store_id):
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

        app.parse_and_save_reviews()

        # refetch to refresh reviews
        app = App.for_play_store_id(play_store_id).first()
        if app.reviews.count() > 0:
            return Response.custom('App reviews with sentiments delivered', {
                'app': app.serialize(),
                'reviews': [r.serialize() for r in app.reviews.all()]
            })


        
