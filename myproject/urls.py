from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

import autocomplete_light
autocomplete_light.autodiscover()

from django.contrib import admin
admin.autodiscover()

from rasikapriya.sitemaps import sitemaps

urlpatterns = patterns('',
    url(r'^$', TemplateView.as_view(template_name='rasikapriya/home_page.html'), name='home'),
    (r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}),
    url(r'^autocomplete/', include('autocomplete_light.urls')),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('rasikapriya.urls')),
)
