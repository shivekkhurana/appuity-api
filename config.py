import os
import urllib.parse
urllib.parse.uses_netloc.append("postgres")

url_str = os.environ.get('DATABASE_URL') or "postgres://shivekkhurana:@localhost:5432/appuity_dev"
url = urllib.parse.urlparse(url_str)

databases = {
	'default': 'main',
    'main': {
        'driver': 'postgres',
        'host': url.hostname,
        'port': url.port,
        'database': url.path[1:],
        'user': url.username,
        'password': url.password
    }
}

google_api_key = 'AIzaSyCxzDCKc1kb6pTcI9bTrSoPuiVf19AJ8R8'