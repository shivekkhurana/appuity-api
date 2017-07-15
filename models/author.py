from .base import Base

class Author(Base):
	__table__ = 'authors'
	__fillable__ = ['name', 'avatar_url']