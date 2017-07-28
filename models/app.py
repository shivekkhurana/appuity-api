from orator.orm import has_many
from .base import Base

class App(Base):
	__table__ = 'apps'
	__fillable__ = [
		'name',
		'category',
		'total_reviews',
		'avg_rating',
		'last_updated',
		'current_version',
		'size',
		'no_of_downloads',
		'offered_by',
		'developer',
		'play_store_id'
	]

	@has_many
	def reviews(self):
		return Review