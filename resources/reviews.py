from flask_restful import Resource
from bs4 import BeautifulSoup
import requests

from models import App,Review

class ReviewsResource(Resource):

    def get(self, play_store_id):

        exists = App.where('play_store_id', '=', play_store_id).first()
        if (exists):
            return {
            	'msg':'Found in the database. No need to crawl',
            	'status':200
            }

        # fetch html from play store
        play_store_html = requests.get('https://play.google.com/store/apps/details?id={}'.format(play_store_id))
        if (play_store_html.status_code != 200):
            return {
                'msg': 'App not found',
                'status': 404
            }

        soup = BeautifulSoup(play_store_html.text, 'html.parser')

        meta_info = soup.select(".meta-info")
        review_authors = soup.select(".author-name")
        review_text = soup.select(".review-body")
        review_date = soup.select(".review-date")
        #review_rating = soup.findAll('div',{"class": "tiny-star"})

        review_s = '{'

        for review,author,date in zip(review_text,review_authors,review_date):
        	review_s+= 'User'+author.text + 'Writes on '+date.text+ '-- '+review.text+ ". "

        review_s+='}'
        
        #print('0th element : '+review_rating[0]['aria-label'])

        # for rating in review_rating:
        # 	print('rating is '+rating['aria-label'])



        print('Number of Reviews is : ',len(review_text))


        return {
            'msg' : 'App found',
            'App Title':str(soup.select(".id-app-title")[0].text),
            'category':str(soup.select(".category")[0].text),
            'Total Reviews':str(soup.select(".reviews-num")[0].text),
            'Average Rating':str(soup.select(".score")[0].text),
            'Last Updated':str(meta_info[0].text),
            'Downloads':str(meta_info[1].text),
            'Developer':str(meta_info[-2].text),
            'Offered By':str(meta_info[-1].text),
            'All Reviews ':str(review_s),


        }

        # We have one more info i.e -- 'date of the review', we can add it if we want. 
        