from google.cloud import language
from google.cloud.gapic.language.v1beta2 import enums
from google.cloud.gapic.language.v1beta2 import language_service_client
from google.cloud.proto.language.v1beta2 import language_service_pb2

from bs4 import BeautifulSoup
import requests,jsonpickle

from models import App,Review,Author
from models.base import getDb

def crawlAndSave(html_text,play_store_id):

    soup = BeautifulSoup(html_text, 'html.parser')
    app = getApp(soup,play_store_id)

    review_details  = soup.findAll('div', {"class": "single-review"})

    db = getDb()
    with db.transaction():
        try:
            app.save()
            saved_app_id = app.id
            for review_detail in review_details:
                author = Author()
                author.name = review_detail.find('span',{"class":"author-name"}).text.strip()
                author.avatar_url = review_detail.find('span',{"class":"responsive-img-hdpi"}).find('span')['style'][21:-1]
                author.save()
                saved_author_id = author.id
                review = Review()
                review.author_id = saved_author_id
                text = review_detail.find('div',{"class":"review-body"}).text.strip()[:-13]
                review.review_text = text
                review.app_id = saved_app_id
                review.analysis = jsonpickle.encode(getReviewAnalysisPractice(text))
                review.date = review_detail.find('span',{"class":"review-date"}).text
                review.rating = review_detail.find('div',{"class":"tiny-star star-rating-non-editable-container"})['aria-label'][6:7]
                review.save()
            return True
        except:
        	print("Something went wrong")
        	return False


    # authors = []
    # for review_detail in review_details:
    #     author = Author()
    #     author.name = review_detail.find('span',{"class":"author-name"}).text.strip()
    #     author.avatar_url = review_detail.find('span',{"class":"responsive-img-hdpi"}).find('span')['style'][21:-1]
    #     authors.append(author)


    # all_reviews = []

    # for review_detail in review_details:
    #     review = Review()
    #     review.author_id = 1
    #     review.review_text = review_detail.find('div',{"class":"review-body"}).text.strip()[:-13]
    #     review.app_id = 3
    #     review.analysis = 1.0
    #     review.date = review_detail.find('span',{"class":"review-date"}).text
    #     review.rating = review_detail.find('div',{"class":"tiny-star star-rating-non-editable-container"})['aria-label'][6:7]
    #     all_reviews.append(review)

def getApp(soup,play_store_id):

    meta_info = soup.findAll('div',{"class": "meta-info"})

    version = ''
    if 'Current Version' in meta_info[2].text:
        version += meta_info[2].text.strip()[17:]
    else:
        version += 'Not Mentioned'

    app = App()
    app.name = soup.select(".id-app-title")[0].text
    app.category = soup.select(".category")[0].text.strip()
    app.total_ratings = soup.select(".reviews-num")[0].text
    app.icon_url = soup.find('img', {"class": "cover-image"})['src']
    app.avg_rating = soup.select(".score")[0].text
    app.last_updated = meta_info[0].text.strip()[8:]
    app.current_version = version
    app.no_of_downloads = meta_info[1].text.strip()[10:]
    app.offered_by = meta_info[-2].text.strip()[11:]
    app.developer = jsonpickle.encode({'email':meta_info[-1].text.strip()[11:]})
    app.play_store_id = play_store_id

    return app

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


def mention_entity(num):
    if(num==0):
        return 'TYPE_UNKNOWN'
    elif(num==1):
        return 'PROPER'
    else:
        return 'COMMON'

def getReviewAnalysis(review_text):

    client = language_service_client.LanguageServiceClient()

    document = language_service_pb2.Document()
    document.content = review_text
    document.type = enums.Document.Type.PLAIN_TEXT
    
    encoding = enums.EncodingType.UTF32

    result = client.analyze_entity_sentiment(document, encoding)

    enum = enums.Entity().Type()
    mention_type = enums.EntityMention().Type()

    all_entities = []

    for entity in result.entities:
        result_json = {}
        result_json['entities'] = {}
        result_json['entities']['name'] = entity.name
        result_json['entities']['type'] = return_entity(entity.type)
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
            result_json['entities']['mention']['type'] = mention_entity(mention.type)
        result_json['entities']['sentiment']['score'] = entity.sentiment.score
        result_json['entities']['sentiment']['magnitude'] = entity.sentiment.magnitude
        all_entities.append(result_json)

    return all_entities


def getReviewAnalysisPractice(review_text):

    all_entities = []

    for i in range(1):
        result_json = {}
        result_json['entities'] = {}
        result_json['entities']['name'] = 'name'
        result_json['entities']['type'] = 2
        result_json['entities']['salience'] = 0.52 
        result_json['entities']['mention'] = {}
        result_json['entities']['mention']['text'] = {}
        result_json['entities']['mention']['sentiment'] = {}
        result_json['entities']['sentiment'] = {}
        for j in range(1):
            result_json['entities']['mention']['text']['Content'] = 'app'
            result_json['entities']['mention']['text']['begin_Offset'] = 112
            result_json['entities']['mention']['sentiment']['magnitude'] = 0.49
            result_json['entities']['mention']['sentiment']['score'] = 0.17
            result_json['entities']['mention']['type'] = 1
        result_json['entities']['sentiment']['score'] = 0.51
        result_json['entities']['sentiment']['magnitude'] = 0.4
        all_entities.append(result_json)

    return all_entities
