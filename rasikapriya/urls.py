
import re
from django.conf.urls import patterns, include, url
from django.core.urlresolvers import reverse_lazy
from .views import (ConcertDateDetail, ConcertList, ConcertTodayArchive,
        ConcertDayArchive, InstrumentDetail, ArtistDetail, ArtistList,
        VenueDetail, FestivalDetail, FestivalList)
from .models import Concert, Artist, Instrument
from bsct import views

YYYY = r'(?P<year>\d{4})'
MM = r'(?P<month>\d{2})'
DD = r'(?P<day>\d{2})'
DATE = r'{0}/{1}/{2}'.format(YYYY, MM, DD)
SLUG = r'(?P<slug>[\w-]+)'

def camelcase_to_underscore(name):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

def myurl(pattern, generic_view_class):
    url_name = camelcase_to_underscore(generic_view_class.__name__)
    return url(pattern, generic_view_class.as_view(), name=url_name)

urlpatterns = patterns('',
    myurl(r'^concerts/upcoming/$',  ConcertList),
    myurl(r'^concerts/today/$', ConcertTodayArchive),
    myurl(r'^concerts/{0}/$'.format(DATE), ConcertDayArchive),
    myurl(r'^concerts/{0}/(?P<pk>\d+)/$'.format(DATE), ConcertDateDetail),

    myurl(r'^artists/$', ArtistList),
    myurl(r'^artists/{0}/$'.format(SLUG), ArtistDetail),

    myurl(r'^instruments/{0}/$'.format(SLUG), InstrumentDetail),

    myurl(r'^venues/{0}/$'.format(SLUG), VenueDetail),

    myurl(r'^festivals/$', FestivalList),
    myurl(r'^festivals/{0}/$'.format(SLUG), FestivalDetail),
)
