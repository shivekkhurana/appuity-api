from flask_restful import Resource, reqparse
from pyquery import PyQuery as pq
from lxml import etree
import requests

from models import App

# List resource
class AppsResource(Resource):
    def get(self):
        return {'msg': 'All apps'}


# Instance resource
class AppResource(Resource):
    def res(self, app):
        return {
            'msg': 'App Data',
            'data': str(app)
        }

    def get(self, play_store_id):
        # check if app already exists in personal database 
        exists = App.where('play_store_id', '=', play_store_id).first()
        if (exists):
            return self.res(exists)

        # fetch html from play store
        play_store_html = requests.get('https://play.google.com/store/apps/details?id={}'.format(play_store_id))
        if (play_store_html.status_code != 200):
            return {
                'msg': 'App not found',
                'status': 404
            }

        #parse app info and save to apps table
        doc = pq(etree.fromstring(play_store_html.text))
        app = App()
        app.name = doc('div.id-app-title')[0].text().strip()
        app.category = doc('a.document-subtitle.category')[0].text().strip()
        app.total_reviews = doc('span.rating-count')[0].text().strip()
        app.avg_rating = doc('div.score')[0].text().strip()
        app.last_updated = doc('div[itemprop=datePublished]')[0].text().strip()
        app.current_version = doc('div[itemprop=softwareVersion]')[0].text().strip()
        # app.size = doc('div[itemprop=datePublished]')[0].text().strip()
        app.no_of_downloads = doc('div[itemprop=numDownloads]')[0].text().strip()
        # app.offered_by = doc('div[itemprop=datePublished]')[0].text().strip()
        # dev_links = doc('a.dev-links')
        # app.developer = {
        #     doc('div[itemprop=datePublished]')[0].text().strip()
        # }
        app.play_store_id = play_store_id
        print(app)

        return {'msg': 'SUccess'}

        # parse authors and save
        # parse reviews
        # for each review, compute sentiments and save to reviews table
        # aggregate and return
        
