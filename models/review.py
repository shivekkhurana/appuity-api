from orator.orm import belongs_to, scope

from .base import Base

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

    @scope
    def with_author(self, query):
    	return query.with_('author')

    @scope
    def with_app(self, query):
    	return query.with_('app')

    @scope
    def for_play_store_id(self, query, play_store_id):
    	return query.where_has('app', lambda q: q.where('play_store_id', '=', play_store_id))
