from google.cloud import language
from google.cloud.gapic.language.v1beta2 import enums
from google.cloud.gapic.language.v1beta2 import language_service_client
from google.cloud.proto.language.v1beta2 import language_service_pb2

from flask_restful import Resource
from bs4 import BeautifulSoup
import requests


from models import App,Review

def return_entity(num):
    if(num==0):
        return 'UNKNOWN'
    elif(num==1):
        return 'PERSON'
    elif(num==2):
        return 'LOCATION'
    elif(num==3):
        return 'ORGANIZATION'
    elif(num==4):
        return 'EVENT'
    elif(num==5):
        return 'WORK_OF_ART'
    elif(num==6):
        return 'CONSUMER_GOOD'
    else:
        return 'OTHER'

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

        # First 6 reviews are featured reviews, they are repeated in the general reviews as well
        # So, we have removed the first 6 reviews.
        author_urls  = soup.findAll('span', {"class": "responsive-img-hdpi"})[6:]
        # if len(author_urls)<1:
        #     return jsonify({'message':'Reviews less than 6'})

        meta_info = soup.select(".meta-info")

        author_names = soup.select(".author-name")
        review_texts = soup.select(".review-body")
        review_date = soup.select(".review-date")
        review_rating = soup.findAll('div',{"class": "review-info-star-rating"})
       
        # Creating a Credentials Object, this one is used when you are making a http request. So not suitable in this file.
        # Approach 5 This file is directly under the Appuity folder. Can change it based on what is best position.
        credential = language.Client.from_service_account_json('..\Appuity-23548e4bd5e5.json')

        # Approach 2
        client = language_service_client.LanguageServiceClient()

        text = 'It App was Very Excellent But i Dont Understand Why You Are Force to \
        Download Nptel All Subject App.\
        i Install This App from last 1 week But Now, when I open this App It Shows Message \
        on Screen is Your App is Expire on 5th May 2017 plz Download Nptel All Subject App? \
        Please Correct This Problem.Thats Why I Give Only 3 star'

        # if isinstance(text, six.binary_type):
        #     text = text.decode('utf-8')

        document = language_service_pb2.Document()
        document.content = text
        document.type = enums.Document.Type.PLAIN_TEXT

        encoding = enums.EncodingType.UTF32
        # if sys.maxunicode == 65535:
        #     encoding = enums.EncodingType.UTF16

        result = client.analyze_entity_sentiment(document, encoding)

        enum = enums.Entity().Type()
        mention_type = enums.EntityMention().Type()

        all_entities = []

        for entity in result.entities:
            result_json = {}
            result_json['entities'] = {}
            result_json['entities']['name'] = entity.name
            result_json['entities']['type'] = entity.type
            result_json['entities']['salience'] = entity.salience 
            result_json['entities']['mention'] = {}
            result_json['entities']['mention']['text'] = {}
            result_json['entities']['mention']['sentiment'] = {}
            result_json['entities']['sentiment'] = {}
            for mention in entity.mentions:
                result_json['entities']['mention']['text']['Content'] = mention.text.content
                result_json['entities']['mention']['text']['begin_Offset'] = mention.text.begin_offset
                result_json['entities']['mention']['sentiment']['magnitude'] = mention.sentiment.magnitude
                result_json['entities']['mention']['sentiment']['score'] = mention.sentiment.score
                result_json['entities']['mention']['type'] = mention.type
            result_json['entities']['sentiment']['score'] = entity.sentiment.score
            result_json['entities']['sentiment']['magnitude'] = entity.sentiment.magnitude
            all_entities.append(result_json)

        all_reviews = [] 

        # Review objects can be created here
        # for i,review,author_name,author_url,date,rating in zip(range(1,len(author_names)),
        #          review_texts,
        #          author_names,
        #          author_urls,
        #          review_date,
        #          review_rating):
        #     author_link = author_url.find('span')['style'][21:-1]
        #     stars = rating.find('div')['aria-label'][6:7]
        #     review_trim = review.text[2:-15]
        #     # document = types.Document(content=review_trim,type=enums.Document.Type.PLAIN_TEXT)
        #     # sentiment = client.analyze_sentiment(document=document).document_sentiment

        #     temp_review = Review()
        #     temp_review.app_id = play_store_id
        #     temp_review.author_id = 1
        #     temp_review.rating = stars
        #     temp_review.review_text = review_trim
        #     temp_review.date = date.text
        #     temp_review.score = 0.0
        #     temp_review.magnitude = 0.0
        #     all_reviews.append(temp_review)
        

        # analysis = jsonpickle.encode(str(result_json))

        return all_entities