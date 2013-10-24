
import sys
import requests
import argparse
from django.conf import settings
import logging
logger = logging.getLogger(__name__)

def geocode(address):
    if not address:
        return None
    params = {
        'address': address,
        'sensor': 'false',
    }
    request = requests.get('https://maps.googleapis.com/maps/api/geocode/json', params=params)
    logger.debug('Geocode query URL {}'.format(request.url))
    response = request.json()
    status = response['status']
    if status != 'OK':
        logger.warning('Geocode was not successful for the following reason: {}'.format(status))
        logger.warning('The address geocoded was {}'.format(address))
        return None
    location = response['results'][0]['geometry']['location']
    return location
#     print response['results'][0]['formatted_address']
#     print response['results'][0]['address_components']

def time_zone(location):
    if not location:
        return None
    latlng = '%f,%f' % (location['lat'], location['lng'])
    params = {
        'location': latlng,
        'timestamp': 0,
        'sensor': 'false',
    }
    request = requests.get('https://maps.googleapis.com/maps/api/timezone/json', params=params)
    response = request.json()
    status = response['status']
    if status != 'OK':
        logger.warning('Timezone query was not successful for the following reason: {}'.format(status))
        logger.warning('The location was {}'.format(latlng))
        return None
    return response['timeZoneId']

def reverse_geocode(location):
    latlng = '%f,%f' % (location['lat'], location['lng'])
    params = {
        'latlng': latlng,
        'sensor': 'false',
    }
    request = requests.get('https://maps.googleapis.com/maps/api/geocode/json', params=params)
    print request.url
    response = request.json()
    status = response['status']
    if status != 'OK':
        print 'Geocode was not successful for the following reason: ', status
        return
    location = response['results'][0]['geometry']['location']
    print response
    print location
    print response['results'][0]['formatted_address']
    print response['results'][0]['address_components']

def get_home_page(artist):
    instruments = u' '.join(unicode(i) for i in artist.instruments)
    search_string = u'%s music %s' % (artist, instruments)
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
    if not artist.instruments:
        return
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

def do_all():
    from .models import Artist
    for artist in Artist.objects.filter(home_page__exact='').filter(description__exact=''):
        update_artist_details(artist)

if __name__ == '__main__':
    do_all()
