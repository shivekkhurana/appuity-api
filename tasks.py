import requests
from invoke import task
import concurrent.futures
import time
import asyncio

@task
def dev(ctx):
    ctx.run("python server.py")

@task
def populate_apps_table(ctx):
    play_store_ids = [
        'com.snapchat.android', 'com.facebook.orca', 'com.whatsapp',
        'com.instagram.android', 'in.amazon.mShop.android.shopping',
        'net.one97.paytm', 'com.zhiliaoapp.musically', 'org.videolan.vlc', 
        'com.pinterest'
    ]

    for i in play_store_ids:
        print('Fetching {}'.format(i))
        requests.get('http://localhost:5000/apps/{}'.format(i))