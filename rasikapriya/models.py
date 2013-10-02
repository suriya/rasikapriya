from django.db import models
from autoslug import AutoSlugField
import string
from .widgets import PlacesAutocompleteWidget

class Instrument(models.Model):
    slug = AutoSlugField(unique=True, populate_from='name')
    name = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name

class Artist(models.Model):
    create_date = models.DateTimeField(auto_now_add=True)
    modify_date = models.DateTimeField(auto_now=True)
    slug = AutoSlugField(unique=True, populate_from='full_name')
    native_place = models.CharField(max_length=255, blank=True)
    initials = models.CharField(max_length=255, blank=True)
    first_name = models.CharField(max_length=255, blank=True)
    middle_name = models.CharField(max_length=255, blank=True)
    last_name = models.CharField(max_length=255, blank=True)
    instruments = models.ManyToManyField(Instrument)
    home_page = models.URLField(blank=True)
    description = models.TextField(blank=True)

    @property
    def full_name(self):
        return string.capwords('%s %s %s %s %s' % (self.native_place,
            self.initials, self.first_name, self.middle_name,
            self.last_name))

    def clean(self):
        from django.core.exceptions import ValidationError
        if not any([ self.first_name, self.middle_name, self.last_name ]):
            raise ValidationError('Artist name cannot be empty.')

    def __unicode__(self):
        return self.full_name

class Venue(models.Model):
    slug = AutoSlugField(unique=True, populate_from='full_address')
    name = models.CharField(max_length=255, blank=True)
    address = models.TextField()
    home_page = models.URLField(blank=True)

    @property
    def full_address(self):
        return '%s %s' % (self.name, self.address)

    def __unicode__(self):
        if self.name:
            return self.name
        return self.address

class Organization(models.Model):
    slug = AutoSlugField(unique=True, populate_from='name')
    name = models.CharField(max_length=255)
    venue = models.ForeignKey(Venue, blank=True, null=True,
            help_text=u'Only if the organization has a physical address')
    home_page = models.URLField(blank=True)
    description = models.TextField(blank=True)

    def __unicode__(self):
        return self.name

class Festival(models.Model):
    slug = AutoSlugField(unique=True, populate_from='full_name')
    name = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    home_page = models.URLField(blank=True)
    description = models.TextField(blank=True)
    venue = models.ForeignKey(Venue, blank=True, null=True,
            help_text=u'If the festival is in a single location')

    @property
    def full_name(self):
        return u'%s (%d)' % (self.name, self.start_date.year)

    def __unicode__(self):
        return self.full_name