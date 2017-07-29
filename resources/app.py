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

        soup = BeautifulSoup(play_store_html.text, 'html.parser')

        meta_info = soup.select(".meta-info")

        version = ''
        if 'Current Version' in meta_info[2].text:
            version += meta_info[2].text
        else:
            version += 'Not Mentioned'

        
        return {
            'msg' : 'App found',
            'text': str(play_store_html),
            'Cover-Image URL':str(soup.find('img', {"class": "cover-image"})['src']),
            'title':str(soup.select(".id-app-title")[0].text),
            'category':str(soup.select(".category")[0].text),
            'Total Reviews':str(soup.select(".reviews-num")[0].text),
            'Average Rating':str(soup.select(".score")[0].text),
            'Last Updated':str(meta_info[0].text),
            'Downloads':str(meta_info[1].text),
            'Offered By':str(meta_info[-2].text),
            'Developer':str(meta_info[-1].text),
            'Current Version':version,
            'Size':'',
            'status': 200
        }

        # app.name = doc('div.id-app-title')[0].text().strip()
        # app.category = doc('a.document-subtitle.category')[0].text().strip()
        # app.total_reviews = doc('span.rating-count')[0].text().strip()
        # app.avg_rating = doc('div.score')[0].text().strip()
        # app.last_updated = doc('div[itemprop=datePublished]')[0].text().strip()
        # app.current_version = doc('div[itemprop=softwareVersion]')[0].text().strip()
        # app.size = doc('div[itemprop=datePublished]')[0].text().strip()
        #app.no_of_downloads = doc('div[itemprop=numDownloads]')[0].text().strip()
        # app.offered_by = doc('div[itemprop=datePublished]')[0].text().strip()
        # dev_links = doc('a.dev-links')
        # app.developer = {
        #     doc('div[itemprop=datePublished]')[0].text().strip()
        # }
        # app.play_store_id = play_store_id
        # print(app)

        

        # parse authors and save
        # parse reviews
        # for each review, compute sentiments and save to reviews table
        # aggregate and return
        
