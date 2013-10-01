
import sys
import requests
import argparse
from django.conf import settings
from rasikapriya.models import Artist, Instrument

# def parse_args():
#     parser = argparse.ArgumentParser(description='Add a new artist')
#     parser.add_argument('--artist', '-a', required=True, help='name of the artist')
#     parser.add_argument('--instruments', '-i', required=True, nargs='+', help='instruments played')
#     return parser.parse_args()

def get_home_page(artist):
    search_string = '%s %s' % (artist.full_name, ' '.join(unicode(i) for i in artist.instruments.all()))
    params = {
        'v': '1.0',
        'q': search_string,
    }
    r = requests.get("http://ajax.googleapis.com/ajax/services/search/web", params=params)
    print r.url
    return [ x['url'] for x in r.json()['responseData']['results']]

def get_url_summary(url):
    params = (
        ('SM_API_KEY', settings.SM_API_KEY,),
        ('SM_LENGTH', 6,),
        ('SM_URL', url,),
    )
    r = requests.get('http://api.smmry.com/', params=params, timeout=20)
    print r.url
    return r.json()['sm_api_content']

def update_artist_details(artist):
    search_results = get_home_page(artist)
    for url in search_results:
        if 'youtube' in url:
            continue
        try:
            summary = get_url_summary(url)
        except KeyError:
            continue
        artist.home_page = url
        artist.description = summary
        artist.save()
        print 'Saved artist details', artist
        break

# if __name__ == '__main__':
#     do_all()
