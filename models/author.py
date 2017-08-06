from orator.orm import has_many

from .base import Base

class Author(Base):
	__table__ = 'authors'
	__fillable__ = ['name', 'avatar_url']

	@has_many
	def reviews(self):
		from .review import Review
		return Review
