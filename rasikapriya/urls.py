
from django.conf.urls import patterns, include, url
from django.core.urlresolvers import reverse_lazy
from .views import ConcertDetailView, ConcertListView
from .models import Concert
from bsct import views

urlpatterns = patterns('',
#     url(r'^concert/list/$',                    ConcertListView.as_view(),   name='concert_list'),
    url(r'^concert/list/$', views.ListView.as_view(model=Concert, paginate_by=10), name='concert_list'),
#     url(r'^concert/detail/(?P<slug>[\w-]+)/$', ConcertDetailView.as_view(), name='concert_detail'),
    url(r'^concert/detail/(?P<pk>\d+)/$', ConcertDetailView.as_view(), name='concert_detail'),
)
