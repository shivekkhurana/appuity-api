from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types

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

        author_names = soup.select(".author-name")
        review_texts = soup.select(".review-body")
        review_date = soup.select(".review-date")
        review_rating = soup.findAll('div',{"class": "review-info-star-rating"})

        # First 6 reviews are featured reviews, they are repeated in the general reviews as well
        # So, we have removed the first 6 reviews.
        author_urls  = soup.findAll('span', {"class": "responsive-img-hdpi"})[6:]
        
        # Creating a Credentials Object, this one is used when you are making a http request. So not suitable in this file.
        # creds = service_account.Credentials.from_service_account_file('..\Appuity-23548e4bd5e5.json')

        # Instantiates a client
        # client = language.LanguageServiceClient(credentials=creds)

        # Approach 5 This file is directly under the Appuity folder. Can change it based on what is best position.
        credential = language.Client.from_service_account_json('..\Appuity-23548e4bd5e5.json')

        # Approach 2
        client = language.LanguageServiceClient()

        # Approach 3
        # client = language.Client.from_service_account_json('..\Appuity-23548e4bd5e5.json')

        # Approach 4
        # client = language.LanguageServiceClient(credentials=creds)

        # Checking client object
        # document = types.Document(content='Not authenticated !!',type=enums.Document.Type.PLAIN_TEXT)
        # print('My client is -- '+str(client.analyze_sentiment(document=document).document_sentiment))

        review_s = '' 

        # Review objects can be created here
        for i,review,author_name,author_url,date,rating in zip(range(1,len(author_names)),
                 review_texts,
                 author_names,
                 author_urls,
                 review_date,
                 review_rating):
            author_link = author_url.find('span')['style'][21:-1]
            stars = rating.find('div')['aria-label'][6:7]
            review_trim = review.text[:-15]
            document = types.Document(content=review_trim,type=enums.Document.Type.PLAIN_TEXT)
            sentiment = client.analyze_sentiment(document=document).document_sentiment
            review_s+= str(i)+' User'+author_name.text + 'With URL '+ author_link + \
            ' Writes on '+date.text+ '-- '+review_trim+ " and gave " + stars + ' stars.' + \
            'Sentiment Score - ' +str(sentiment.score)+' Emotional Magnitude -- '+str(sentiment.magnitude)+' '
        
        
        return {
            'msg' : 'App found',
            'App Title':str(soup.select(".id-app-title")[0].text),
            'category':str(soup.select(".category")[0].text),
            'Total Reviews':str(soup.select(".reviews-num")[0].text),
            'Average Rating':str(soup.select(".score")[0].text),
            'Last Updated':str(meta_info[0].text),
            'Downloads':str(meta_info[1].text),
            'Developer':str(meta_info[-1].text),
            'Offered By':str(meta_info[-2].text),
            'All Reviews ':str(review_s),
            
        }

        # We have one more info i.e -- 'date of the review', we can add it if we want. 
        