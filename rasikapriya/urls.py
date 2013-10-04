
import re
from django.conf.urls import patterns, include, url
from django.core.urlresolvers import reverse_lazy
from .views import (ConcertDateDetail, ConcertList, ConcertTodayArchive,
        ConcertDayArchive, InstrumentDetail, ArtistDetail)
from .models import Concert, Artist, Instrument
from bsct import views

YYYY = r'(?P<year>\d{4})'
MM = r'(?P<month>\d{2})'
DD = r'(?P<day>\d{2})'
DATE = r'{0}/{1}/{2}'.format(YYYY, MM, DD)

def camelcase_to_underscore(name):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

def myurl(pattern, generic_view_class):
    url_name = camelcase_to_underscore(generic_view_class.__name__)
    return url(pattern, generic_view_class.as_view(), name=url_name)

#     myurl(r'^concerts/{0}/{1}/'.format(YYYY, MM), ConcertMonthArchive),
urlpatterns = patterns('',
    myurl(r'^concerts/upcoming/$',  ConcertList),
    myurl(r'^concerts/today/$', ConcertTodayArchive),
    myurl(r'^concerts/{0}/$'.format(DATE), ConcertDayArchive),
    myurl(r'^concerts/{0}/(?P<pk>\d+)/$'.format(DATE), ConcertDateDetail),

    url(r'^artist/list/$', views.ListView.as_view(model=Artist, paginate_by=10), name='artist_list'),
    url(r'^artist/detail/(?P<slug>[\w-]+)/$', ArtistDetail.as_view(), name='artist_detail'),

    url(r'^instrument/detail/(?P<slug>[\w-]+)/$', InstrumentDetail.as_view(), name='instrument_detail'),
)
