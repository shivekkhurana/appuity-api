import json
from bs4 import BeautifulSoup
from orator.orm import has_many, scope

from .base import Base

class App(Base):
    __table__ = 'apps'
    __fillable__ = [
        'name', 'category', 'total_ratings', 'icon_url', 'avg_rating', 'last_updated',
        'current_version', 'no_of_downloads', 'offered_by','developer','play_store_id',
        'play_store_html'
    ]

    @has_many
    def reviews(self):
        from .review import Review
        return Review

    def serialize(self):
        app = super(App, self).serialize()
        return {k:v for k, v in app.items() if k not in ['play_store_html']}

    def parse_html_and_save(self, html, play_store_id):
        soup = BeautifulSoup(html, 'html.parser')
        meta_info = soup.findAll('div', {'class': 'meta-info'})

        version = ''
        if 'Current Version' in meta_info[2].text:
            version += meta_info[2].text.strip()[17:]
        else:
            version += 'Not Mentioned'
        
        self.name = soup.select('.id-app-title')[0].text
        self.category = soup.select('.category')[0].text.strip()
        self.total_ratings = soup.select('.reviews-num')[0].text
        self.icon_url = soup.find('img', {'class': 'cover-image'})['src']
        self.avg_rating = soup.select('.score')[0].text
        self.last_updated = meta_info[0].text.strip()[8:]
        self.current_version = version
        self.no_of_downloads = meta_info[1].text.strip()[10:]
        self.offered_by = meta_info[-2].text.strip()[11:]
        self.developer = json.dumps({'email': meta_info[-1].text.strip()[11:]})
        self.play_store_id = play_store_id
        self.play_store_html = html
        self.save()

        return self

    def parse_and_save_reviews(self):
        from .author import Author
        from .review import Review
        
        soup = BeautifulSoup(self.play_store_html, 'html.parser')
        review_details  = soup.findAll('div', {"class": "single-review"})

        parsed = [{
            'author': {
                'name': r.find('span', {"class":"author-name"}).text.strip(),
                'avatar_url': r.find('span',{"class":"responsive-img-hdpi"}).find('span')['style'][21:-1]
            },
            'review': {
                'review_text': r.find('div',{"class":"review-body"}).text.strip()[:-13],
                'date': r.find('span',{"class":"review-date"}).text,
                'rating': r.find('div',{"class":"tiny-star star-rating-non-editable-container"})['aria-label'][6:7]
            }
        } for r in review_details]

        authors = (p['author'] for p in parsed)
        author_ids = [Author().find_or_create(a).id for a in authors]
        reviews = [p['review'] for p in parsed]
        reviews_with_relations = [dict(review, **{
            'app_id': self.id,
            'author_id': author_ids[i]
        }) for i, review in enumerate(reviews)]

        Review().fetch_analysis_and_save(reviews_with_relations)
        return self

    @scope
    def for_play_store_id(self, query, play_store_id):
        return query.where('play_store_id', '=', play_store_id)
