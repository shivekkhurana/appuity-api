from orator.orm import belongs_to, scope
import json
import requests
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

    def fetch_analysis_and_save(reviews):
        async def main():
            with concurrent.futures.ThreadPoolExecutor(max_workers=24) as executor:
                loop = asyncio.get_event_loop()
                sentiment_futures = [loop.run_in_executor(
                    executor, 
                    requests.post, 
                    'https://language.googleapis.com/v1/documents:analyzeSentiment?key={}'.format(google_api_key),
                    {
                        "encodingType": "UTF8",
                        "document": {
                            "type": "PLAIN_TEXT",
                            "content": r['review_text']
                        }
                    }
                ) for r in reviews]
                
                entity_futures = [loop.run_in_executor(
                    executor, 
                    requests.post, 
                    'https://language.googleapis.com/v1/documents:analyzeEntities?key={}'.format(google_api_key),
                    {
                        "encodingType": "UTF8",
                        "document": {
                            "type": "PLAIN_TEXT",
                            "content": r['review_text']
                        }
                    }
                ) for r in reviews]

                all_futures = sentiment_futures + entity_futures
                responses = [response for response in await asyncio.gather(*all_futures)]
                analysed_reviews = [dict(r, **{
                    'analysis': json.dumps({
                        'sentiment': responses[i] 
                        'entity': response[len(reviews) + i]
                    })
                }) for i, r in enumerate(reviews)]
                self.bulk_insert(analysed_reviews)

        loop = asyncio.get_event_loop()
        loop.run_until_complete(main())

    @scope
    def with_author(self, query):
    	return query.with_('author')

    @scope
    def with_app(self, query):
    	return query.with_('app')

    @scope
    def for_play_store_id(self, query, play_store_id):
    	return query.where_has('app', lambda q: q.where('play_store_id', '=', play_store_id))
