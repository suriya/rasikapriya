
from django.core.urlresolvers import reverse
from django.db import models
from autoslug import AutoSlugField
import string
from .widgets import PlacesAutocompleteWidget
from django.core.exceptions import ValidationError
import urllib
from .utils import geocode, time_zone
import pytz
from django.conf import settings
import datetime

class Instrument(models.Model):
    slug = AutoSlugField(unique=True, populate_from='name')
    name = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('instrument_detail', kwargs={ 'slug': self.slug })

class Artist(models.Model):
    create_date = models.DateTimeField(auto_now_add=True)
    modify_date = models.DateTimeField(auto_now=True)
    slug = AutoSlugField(unique=True, populate_from='full_name')
    native_place = models.CharField(max_length=255, blank=True)
    initials = models.CharField(max_length=255, blank=True)
    first_name = models.CharField(max_length=255, blank=True)
    middle_name = models.CharField(max_length=255, blank=True)
    last_name = models.CharField(max_length=255, blank=True)
    home_page = models.URLField(blank=True)
    description = models.TextField(blank=True)
    band_members = models.ManyToManyField('self', symmetrical=False, blank=True)

    @property
    def instruments(self):
        return Instrument.objects.filter(performance__artist=self).distinct()

    @property
    def full_name(self):
        return string.capwords('%s %s %s %s %s' % (self.native_place,
            self.initials, self.first_name, self.middle_name,
            self.last_name))

    def clean(self):
        if not any([ self.first_name, self.middle_name, self.last_name ]):
            raise ValidationError('Artist name cannot be empty.')

    def __unicode__(self):
        return self.full_name

    def get_absolute_url(self):
        return reverse('artist_detail', kwargs={ 'slug': self.slug })

class Venue(models.Model):
    create_date = models.DateTimeField(auto_now_add=True)
    modify_date = models.DateTimeField(auto_now=True)
    slug = AutoSlugField(unique=True, populate_from='full_address')
    name = models.CharField(max_length=255, blank=True)
    address = models.TextField()
    home_page = models.URLField(blank=True)
    time_zone = models.CharField(max_length=255, editable=False, blank=True)

    def clean(self):
        location = geocode(self.address)
        tz_name = time_zone(location)
        if tz_name:
            self.time_zone = tz_name

    @property
    def full_address(self):
        return '%s %s' % (self.name, self.address)

    def __unicode__(self):
        if self.name:
            return self.name
        return self.address

    def static_map_url(self):
        params = (
            ('sensor',  'false'),
            ('size',    '400x280'),
            ('center',  self.address),
            ('markers', self.address),
        )
        return 'http://maps.googleapis.com/maps/api/staticmap?%s' % urllib.urlencode(params)

    def maps_url(self):
        params = (
            ('q', self.address),
        )
        return 'http://maps.google.com/?%s' % urllib.urlencode(params)

    def get_absolute_url(self):
        return reverse('venue_detail', kwargs={ 'slug': self.slug })

class Organization(models.Model):
    create_date = models.DateTimeField(auto_now_add=True)
    modify_date = models.DateTimeField(auto_now=True)
    slug = AutoSlugField(unique=True, populate_from='name')
    name = models.CharField(max_length=255)
    venue = models.ForeignKey(Venue, blank=True, null=True,
            help_text=u'Only if the organization has a physical address')
    home_page = models.URLField(blank=True)
    description = models.TextField(blank=True)

    def __unicode__(self):
        return self.name

class Festival(models.Model):
    create_date = models.DateTimeField(auto_now_add=True)
    modify_date = models.DateTimeField(auto_now=True)
    slug = AutoSlugField(unique=True, populate_from='full_name')
    name = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    organization = models.ForeignKey(Organization, blank=True, null=True,
            help_text=u'The organizer of the festival.')
    home_page = models.URLField(blank=True)
    description = models.TextField(blank=True)
    venue = models.ForeignKey(Venue, blank=True, null=True,
            help_text=u'If the festival is in a single location')

    @property
    def full_name(self):
        return u'%s (%d)' % (self.name, self.start_date.year)

    def __unicode__(self):
        return self.full_name

    def get_absolute_url(self):
        return reverse('festival_detail', kwargs={ 'slug': self.slug })

class Concert(models.Model):
    create_date = models.DateTimeField(auto_now_add=True)
    modify_date = models.DateTimeField(auto_now=True)
    festival = models.ForeignKey(Festival, blank=True, null=True,
            help_text=u'If the concert is part of a festival')
    organization = models.ForeignKey(Organization, blank=True, null=True,
            help_text=u"""If the concert is not a part of a festival, the
            details of the organizer""")
    venue = models.ForeignKey(Venue, blank=True, null=True,
            related_name='+',
            help_text=u"""For a concert's venue, we try the following
            options. 1. the venue of the festival, if the concert is part
            of a festival with a single venue; 2. the venue of the
            organization, if available; 3; the concert's venue itself, in
            which case, enter the details here.""")
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField(blank=True, null=True)
    aware_start_time = models.DateTimeField(editable=False)
    aware_end_time = models.DateTimeField(blank=True, null=True, editable=False)
    artists = models.ManyToManyField(Artist, through='Performance')
    cached_venue = models.ForeignKey(Venue, editable=False,
            help_text=u"""The venue could come from either self.venue,
            or from self.festival.venue, or self.organization.venue. We
            cache the result here so that Venue.concert_set.all() works.
            """)

    def _lookup_venue(self):
        if self.venue:
            return self.venue
        elif self.festival and self.festival.venue:
            return self.festival.venue
        elif self.organization and self.organization.venue:
            return self.organization.venue
        else:
            return None

    def clean(self):
        self.cached_venue = self._lookup_venue()
        if not self.cached_venue:
            raise ValidationError(u"""Concert needs to have a venue; either
                    by itself, or from the concert's festival, or from the
                    concert's organizer.""")
        time_zone = self.cached_venue.time_zone
        if not time_zone:
            time_zone = settings.TIME_ZONE
        tzobj = pytz.timezone(time_zone)
        self.aware_start_time = tzobj.localize(datetime.datetime.combine(self.date, self.start_time))
        if self.end_time:
            self.aware_end_time = tzobj.localize(datetime.datetime.combine(self.date, self.end_time))

    def __unicode__(self):
        artists = ', '.join(unicode(a) for a in self.artists.all())
        return u'%s; %s; %s' % (artists, self.cached_venue, self.date)

    def get_absolute_url(self):
        kwargs = {
            'pk'    : self.pk,
            'year'  : self.date.year,
            'month' : '%02d' % self.date.month,
            'day'   : '%02d' % self.date.day,
        }
        return reverse('concert_date_detail', kwargs=kwargs)

    @property
    def main_performer(self):
        return self.performance_set.all()[0]

    @property
    def title(self):
        return unicode(self)

class Performance(models.Model):
    create_date = models.DateTimeField(auto_now_add=True)
    modify_date = models.DateTimeField(auto_now=True)
    artist = models.ForeignKey(Artist)
    concert = models.ForeignKey(Concert)
    instrument = models.ForeignKey(Instrument)

    def __unicode__(self):
        return u'%s %s' % (self.artist, self.instrument)
