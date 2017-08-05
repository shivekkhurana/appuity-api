from flask_restful import Resource
import requests
from utils import Response

from models import App

# List resource
class AppsResource(Resource):
    def get(self):
        return Response.collection('All apps', App.all())


# Instance resource
class AppResource(Resource):
    
    def get(self, play_store_id):
        app_found = App.for_play_store_id(play_store_id).first()
        if (app_found):
            return Response.model('Delivered', app_found)

        try:
            res = requests.get('https://play.google.com/store/apps/details?id={}'.format(play_store_id))
            if (res.status_code != 200):
                return Response.error('No app found for app id {}'.format(play_store_id), 404)
        except requests.exceptions.ConnectionError:
            return Response.error('Unable to fetch app from playstore, please try again after sometime', 500)

        new_app = App()
        new_app.parse_html_and_save(res.text, play_store_id)

        return Response.model('Delivered', new_app)
