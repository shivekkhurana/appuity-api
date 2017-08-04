from google.cloud import language
from google.cloud.gapic.language.v1beta2 import enums
from google.cloud.gapic.language.v1beta2 import language_service_client
from google.cloud.proto.language.v1beta2 import language_service_pb2

from flask_restful import Resource
from bs4 import BeautifulSoup
import requests

from models.base import getDb
from models import App,Review
from .service import crawlAndSave



class ReviewsResource(Resource):

    def serialize(self,review):
        return {
            'app_id':review.app_id,
            'author_id':review.author_id,
            'author_name':review.name,
            'author_url':review.avatar_url,
            'rating':review.rating,
            'review_text':review.review_text,
            'date':review.date,
            'review_analysis':review.analysis,
        }

    def getAllReviews(self,app):
        db_app_id = app.id
        db = getDb()
        return db.table('reviews').join('authors', 'authors.id', '=', 'reviews.author_id').where('app_id','=',db_app_id).get()

    def get(self, play_store_id):

        exists = App.where('play_store_id', '=', play_store_id).first()
        if (exists):
            reviews = self.getAllReviews(exists)
            # reviews = Review.where('app_id','=',exists_id).get()
            return [self.serialize(review) for review in reviews]


        try:
            # fetch html from play store
            play_store_html = requests.get('https://play.google.com/store/apps/details?id={}'.format(play_store_id))
            if (play_store_html.status_code != 200):
                return {
                    'msg': 'No App found. Please Check ID.',
                    'status': 404
                }
        except requests.exceptions.ConnectionError:
            return {
                    'message':'Could not fulfill request. Try after some time',
                    'status' : 500
            }

        app_insert = crawlAndSave(play_store_html.text,play_store_id)

        if (app_insert):
            inserted_app = App.where('play_store_id', '=', play_store_id).first()
            reviews = self.getAllReviews(inserted_app)
            return [self.serialize(review) for review in reviews]
        else:
            return {'message':'Some error occured while completeing request','status':500}

        # soup = BeautifulSoup(play_store_html.text, 'html.parser')

        # review_details  = soup.findAll('div', {"class": "single-review"})

        # all_reviews = []

        # for review_detail in review_details:
        #     review = Review()
        #     review.author_id = review_detail.find('span',{"class":"responsive-img-hdpi"}).find('span')['style'][21:-1]
        #     review.review_text = review_detail.find('div',{"class":"review-body"}).text.strip()[:-13]
        #     review.app_id = review_detail.find('span',{"class":"author-name"}).text.strip()
        #     review.analysis = 1.0
        #     review.date = review_detail.find('span',{"class":"review-date"}).text
        #     review.rating = review_detail.find('div',{"class":"tiny-star star-rating-non-editable-container"})['aria-label'][6:7]
        #     all_reviews.append(review)

        # return [review.serialize for review in all_reviews]

        # # Creating a Credentials Object, this one is used when you are making a http request. So not suitable in this file.
        # # Approach 5 This file is directly under the Appuity folder. Can change it based on what is best position.
        # credential = language.Client.from_service_account_json('..\Appuity-23548e4bd5e5.json')

        # # Approach 2
        # client = language_service_client.LanguageServiceClient()

        # text = 'It App was Very Excellent But i Dont Understand Why You Are Force to \
        # Download Nptel All Subject App.\
        # i Install This App from last 1 week But Now, when I open this App It Shows Message \
        # on Screen is Your App is Expire on 5th May 2017 plz Download Nptel All Subject App? \
        # Please Correct This Problem.Thats Why I Give Only 3 star'

        # # if isinstance(text, six.binary_type):
        # #     text = text.decode('utf-8')

        # document = language_service_pb2.Document()
        # document.content = text
        # document.type = enums.Document.Type.PLAIN_TEXT

        # encoding = enums.EncodingType.UTF32
        # # if sys.maxunicode == 65535:
        # #     encoding = enums.EncodingType.UTF16

        # result = client.analyze_entity_sentiment(document, encoding)

        # enum = enums.Entity().Type()
        # mention_type = enums.EntityMention().Type()

        # all_entities = []

        # for entity in result.entities:
        #     result_json = {}
        #     result_json['entities'] = {}
        #     result_json['entities']['name'] = entity.name
        #     result_json['entities']['type'] = entity.type
        #     result_json['entities']['salience'] = entity.salience 
        #     result_json['entities']['mention'] = {}
        #     result_json['entities']['mention']['text'] = {}
        #     result_json['entities']['mention']['sentiment'] = {}
        #     result_json['entities']['sentiment'] = {}
        #     for mention in entity.mentions:
        #         result_json['entities']['mention']['text']['Content'] = mention.text.content
        #         result_json['entities']['mention']['text']['begin_Offset'] = mention.text.begin_offset
        #         result_json['entities']['mention']['sentiment']['magnitude'] = mention.sentiment.magnitude
        #         result_json['entities']['mention']['sentiment']['score'] = mention.sentiment.score
        #         result_json['entities']['mention']['type'] = mention.type
        #     result_json['entities']['sentiment']['score'] = entity.sentiment.score
        #     result_json['entities']['sentiment']['magnitude'] = entity.sentiment.magnitude
        #     all_entities.append(result_json)

        # return all_entities

        # Review objects can be created here
        # for i,review,author_name,author_url,date,rating in zip(range(1,len(author_names)),
        #          review_texts,
        #          author_names,
        #          author_urls,
        #          review_date,
        #          review_rating):
        #     author_link = author_url.find('span')['style'][21:-1]
        #     stars = rating.find('div')['aria-label'][6:7]
        #     review_trim = review.text.strip()[:-13]
        #     name = author_name.text.strip()
        #     # document = types.Document(content=review_trim,type=enums.Document.Type.PLAIN_TEXT)
        #     # sentiment = client.analyze_sentiment(document=document).document_sentiment

        #     temp_review = Review()
        #     temp_review.app_id = play_store_id
        #     temp_review.author_id = name
        #     temp_review.rating = stars
        #     temp_review.review_text = review_trim
        #     temp_review.date = date.text
        #     temp_review.analysis = 0.0
        #     all_reviews.append(temp_review)
        

        # analysis = jsonpickle.encode(str(result_json))

        # return [review.serialize for review in all_reviews]
