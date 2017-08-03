from bs4 import BeautifulSoup
import requests,jsonpickle

from models import App,Review,Author
from models.base import getDb

def crawlAndSave(html_text,play_store_id):

    soup = BeautifulSoup(html_text, 'html.parser')
    meta_info = soup.findAll('div',{"class": "meta-info"})

    version = ''
    if 'Current Version' in meta_info[2].text:
        version += meta_info[2].text.strip()[17:]
    else:
        version += 'Not Mentioned'

    app = App()
    app.name = soup.select(".id-app-title")[0].text
    app.category = soup.select(".category")[0].text.strip()
    app.total_ratings = soup.select(".reviews-num")[0].text
    app.icon_url = soup.find('img', {"class": "cover-image"})['src']
    app.avg_rating = soup.select(".score")[0].text
    app.last_updated = meta_info[0].text.strip()[8:]
    app.current_version = version
    app.no_of_downloads = meta_info[1].text.strip()[10:]
    app.offered_by = meta_info[-2].text.strip()[11:]
    app.developer = jsonpickle.encode({'email':meta_info[-1].text.strip()[11:]})
    app.play_store_id = play_store_id

    # app.save()

    # return True

    review_details  = soup.findAll('div', {"class": "single-review"})

    db = getDb()
    with db.transaction():
    	app.save()
    	saved_app_id = app.id
    	for review_detail in review_details:
            author = Author()
            author.name = review_detail.find('span',{"class":"author-name"}).text.strip()
            author.avatar_url = review_detail.find('span',{"class":"responsive-img-hdpi"}).find('span')['style'][21:-1]
            author.save()
            saved_author_id = author.id
            review = Review()
            review.author_id = saved_author_id
            review.review_text = review_detail.find('div',{"class":"review-body"}).text.strip()[:-13]
            review.app_id = saved_app_id
            review.analysis = jsonpickle.encode({'sentiment':0.6,'magnitude':0.9})
            review.date = review_detail.find('span',{"class":"review-date"}).text
            review.rating = review_detail.find('div',{"class":"tiny-star star-rating-non-editable-container"})['aria-label'][6:7]
            review.save()
    return True
    # return False


    # authors = []
    # for review_detail in review_details:
    #     author = Author()
    #     author.name = review_detail.find('span',{"class":"author-name"}).text.strip()
    #     author.avatar_url = review_detail.find('span',{"class":"responsive-img-hdpi"}).find('span')['style'][21:-1]
    #     authors.append(author)


    # all_reviews = []

    # for review_detail in review_details:
    #     review = Review()
    #     review.author_id = 1
    #     review.review_text = review_detail.find('div',{"class":"review-body"}).text.strip()[:-13]
    #     review.app_id = 3
    #     review.analysis = 1.0
    #     review.date = review_detail.find('span',{"class":"review-date"}).text
    #     review.rating = review_detail.find('div',{"class":"tiny-star star-rating-non-editable-container"})['aria-label'][6:7]
    #     all_reviews.append(review)


def getApp(text,id):
	app_inserted = crawlAndSave(text,id)
	return app_inserted
