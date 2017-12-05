from orator.orm import belongs_to, scope
import json
import requests
from promise import Promise
from aiohttp import ClientSession
import asyncio
import concurrent.futures

from .base import Base
from config import google_api_key

class Review(Base):
    __table__ = 'reviews'
    __fillable__ = ['app_id', 'author_id','rating','review_text','date','analysis']

    @belongs_to
    def author(self):
        from .author import Author
        return Author

    @belongs_to
    def app(self):
        from .app import App
        return App

    # def fetch_analysis_and_save(self, reviews):
    #     def post(url, data):
    #         def resolver(resolve, reject):
    #             res = requests.post(url, json=data)
    #             if (res.status_code == 200):
    #                 resolve(res.text)
    #             else:
    #                 reject(res.text)

    #         return Promise(resolver)
    
    #     # sentiment_promises = [post(
    #     #     session,
    #     #     'https://language.googleapis.com/v1/documents:analyzeSentiment?key={}'.format(google_api_key),
    #     #     {
    #     #         "encodingType": "UTF8",
    #     #         "document": {
    #     #             "type": "PLAIN_TEXT",
    #     #             "content": r['review_text']
    #     #         }
    #     #     }
    #     # ) for r in reviews]

    #     entity_promises = [post(
    #         'https://language.googleapis.com/v1/documents:analyzeEntities?key={}'.format(google_api_key),
    #         {
    #             "encodingType": "UTF8",
    #             "document": {
    #                 "type": "PLAIN_TEXT",
    #                 "content": r['review_text']
    #             }
    #         }
    #     ) for r in reviews]

    #     entity_res = Promise.all(entity_promises).then(lambda res: print(res))
    #     print(entity_res)

    #     # print([r.text for r in entity_res])

    def fetch_analysis_and_save(self, reviews):
        async def process_reviews():
            with concurrent.futures.ThreadPoolExecutor(max_workers=24) as executor:
                def sync_get_sentiment_analysis(review):
                    return requests.post(
                        'https://language.googleapis.com/v1/documents:analyzeSentiment?key={}'.format(google_api_key),
                        json={
                            "encodingType": "UTF8",
                            "document": {
                                "type": "PLAIN_TEXT",
                                "content": review['review_text']
                            }
                        }
                    )

                def sync_get_entity_analysis(review):
                    return requests.post(
                        'https://language.googleapis.com/v1/documents:analyzeEntities?key={}'.format(google_api_key),
                        json={
                            "encodingType": "UTF8",
                            "document": {
                                "type": "PLAIN_TEXT",
                                "content": review['review_text']
                            }
                        }
                    )

                sentiment_futures = [loop.run_in_executor(executor, sync_get_sentiment_analysis, r) for r in reviews]
                entity_futures = [loop.run_in_executor(executor, sync_get_entity_analysis, r) for r in reviews]

                sentiment_responses = [response for response in await asyncio.gather(*sentiment_futures)]
                entity_responses = [response for response in await asyncio.gather(*entity_futures)]
                analysed_reviews = [dict(r, **{
                    'analysis': json.dumps({
                        'sentiment': sentiment_responses[i].json(),
                        'entity': entity_responses[i].json()
                    })
                }) for i, r in enumerate(reviews)]
                self.bulk_insert(analysed_reviews)

        loop = asyncio.get_event_loop_policy().new_event_loop()
        loop.run_until_complete(process_reviews())

    @scope
    def with_author(self, query):
    	return query.with_('author')

    @scope
    def with_app(self, query):
    	return query.with_('app')

    @scope
    def for_play_store_id(self, query, play_store_id):
    	return query.where_has('app', lambda q: q.where('play_store_id', '=', play_store_id))
