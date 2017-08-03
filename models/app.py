from orator.orm import has_many
from .base import Base

class App(Base):
    __table__ = 'apps'
    __fillable__ = [
        'name',
        'category',
        'total_ratings',
        'icon_url',
        'avg_rating',
        'last_updated',
        'current_version',
        'no_of_downloads',
        'offered_by',
        'developer',
        'play_store_id'
    ]

    @has_many
    def reviews(self):
        return Review

    @property
    def serialize(self):
        return {
            'name':self.name,
            'category':self.category,
            'total_ratings':self.total_ratings,
            'icon_url':self.icon_url,
            'average_rating':self.avg_rating,
            'last_updated':self.last_updated,
            'current_version':self.current_version,
            'no_of_downloads':self.no_of_downloads,
            'offered_by':self.offered_by,
            'developer':self.developer,
            'play_store_id':self.play_store_id,
        }