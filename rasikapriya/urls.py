
from django.conf.urls import patterns, include, url
from django.core.urlresolvers import reverse_lazy
from .views import (ConcertDetailView, ConcertListView,
        InstrumentDetailView, ArtistDetailView)
from .models import Concert, Artist, Instrument
from bsct import views

urlpatterns = patterns('',
#     url(r'^concert/list/$',                    ConcertListView.as_view(),   name='concert_list'),
    url(r'^concert/list/$', views.ListView.as_view(model=Concert, paginate_by=10), name='concert_list'),
    url(r'^concert/detail/(?P<pk>\d+)/$', ConcertDetailView.as_view(), name='concert_detail'),
    url(r'^artist/list/$', views.ListView.as_view(model=Artist, paginate_by=10), name='artist_list'),
    url(r'^artist/detail/(?P<slug>[\w-]+)/$', ArtistDetailView.as_view(), name='artist_detail'),
    url(r'^instrument/detail/(?P<slug>[\w-]+)/$', InstrumentDetailView.as_view(), name='instrument_detail'),
)
