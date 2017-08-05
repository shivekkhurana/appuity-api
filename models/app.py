import json
from bs4 import BeautifulSoup
from orator.orm import has_many

from .base import Base

class App(Base):
    __table__ = 'apps'
    __fillable__ = [
        'name', 'category', 'total_ratings', 'icon_url', 'avg_rating', 'last_updated',
        'current_version', 'no_of_downloads', 'offered_by','developer','play_store_id'
    ]

    @has_many
    def reviews(self):
        return Review

    def parse_html_and_save(self, html, play_store_id):
        soup = BeautifulSoup(html, 'html.parser')
        meta_info = soup.findAll('div',{"class": "meta-info"})

        version = ''
        if 'Current Version' in meta_info[2].text:
            version += meta_info[2].text.strip()[17:]
        else:
            version += 'Not Mentioned'
        
        self.name = soup.select(".id-app-title")[0].text
        self.category = soup.select(".category")[0].text.strip()
        self.total_ratings = soup.select(".reviews-num")[0].text
        self.icon_url = soup.find('img', {"class": "cover-image"})['src']
        self.avg_rating = soup.select(".score")[0].text
        self.last_updated = meta_info[0].text.strip()[8:]
        self.current_version = version
        self.no_of_downloads = meta_info[1].text.strip()[10:]
        self.offered_by = meta_info[-2].text.strip()[11:]
        self.developer = json.dumps({'email': meta_info[-1].text.strip()[11:]})
        self.play_store_id = play_store_id
        self.save()

        return self
