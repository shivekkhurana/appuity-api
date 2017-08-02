from flask import jsonify
from flask_restful import Resource, reqparse
from bs4 import BeautifulSoup
import requests

from models import App

# List resource
class AppsResource(Resource):
    def get(self):
        return {'msg': 'All apps'}


# Instance resource
class AppResource(Resource):
    
    def get(self, play_store_id):
        # check if app already exists in personal database 
        app_found = App.where('play_store_id', '=', play_store_id).first()
        if (app_found):
            return jsonify(app_found.serialize)

        # fetch html from play store
        play_store_html = requests.get('https://play.google.com/store/apps/details?id={}'.format(play_store_id))
        if (play_store_html.status_code != 200):
            return {
                'msg': 'App not found',
                'status': 404
            }

        soup = BeautifulSoup(play_store_html.text, 'html.parser')

        meta_info = soup.findAll('div',{"class": "meta-info"})

        version = ''
        if 'Current Version' in meta_info[2].text:
            version += meta_info[2].text.strip()[17:]
        else:
            version += 'Not Mentioned'

        app = App()
        app.name = str(soup.select(".id-app-title")[0].text)
        app.category = str(soup.select(".category")[0].text.strip())
        app.total_reviews = str(soup.select(".reviews-num")[0].text)
        app.icon_url = str(soup.find('img', {"class": "cover-image"})['src'])
        app.avg_rating = str(soup.select(".score")[0].text)
        app.last_updated = str(meta_info[0].text.strip()[8:])
        app.current_version = version
        app.no_of_downloads = str(meta_info[1].text.strip()[10:])
        app.offered_by = str(meta_info[-2].text.strip()[11:])
        app.developer = str(meta_info[-1].text.strip()[11:])
        app.play_store_id = play_store_id

        return ({'app_details':app.serialize})

        # parse authors and save
        # parse reviews
        # for each review, compute sentiments and save to reviews table
        # aggregate and return
        
