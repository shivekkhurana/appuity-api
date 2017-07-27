from orator.orm import belongs_to
from .base import Base

class Review(Base):
	__table__ = 'reviews'
	__fillable__ = ['app_id', 'author_url','rating','review_text']

    @belongs_to
    def author(self):
        return Author

    @belongs_to
    def app(self):
        return App