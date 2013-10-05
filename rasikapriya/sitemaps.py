
from django.contrib.sitemaps import Sitemap
from .models import Concert, Artist, Venue

class ConcertSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.5

    def items(self):
        return Concert.objects.all()

    def lastmod(self, obj):
        return obj.modify_date

class ArtistSiteMap(Sitemap):
    changefreq = "daily"
    priority = 0.5

    def items(self):
        return Artist.objects.all()

    def lastmod(self, obj):
        return obj.modify_date

class VenueSiteMap(Sitemap):
    changefreq = "daily"
    priority = 0.5

    def items(self):
        return Venue.objects.all()

    def lastmod(self, obj):
        return obj.modify_date

sitemaps = {
    'concert': ConcertSitemap,
    'artist': ArtistSiteMap,
    'venue': VenueSiteMap,
}
