
from django.views.generic import (DateDetailView, DetailView, ListView,
        DayArchiveView, TodayArchiveView)
from .models import Concert, Artist, Instrument, Venue
from django.shortcuts import get_object_or_404

class DateFormat:
    year_format = '%Y'
    month_format = '%m'
    day_format = '%d'

class ConcertDateDetail(DateFormat, DetailView):
    model = Concert
    context_object_name = 'concert'
    date_field = 'date'

class ConcertDayArchive(DateFormat, DayArchiveView):
    model = Concert
    date_field = 'date'
    context_object_name = 'concert_list'
    paginate_by = 10
    allow_future = True
    template_name = 'rasikapriya/concert_list.html'

class ConcertTodayArchive(TodayArchiveView):
    model = Concert
    date_field = 'date'
    context_object_name = 'concert_list'
    paginate_by = 10
    allow_future = True
    template_name = 'rasikapriya/concert_list.html'

class ConcertList(ListView):
    model = Concert
    paginate_by = 10
    context_object_name = 'concert_list'

class InstrumentDetail(ListView):
    # Making this a ListView so that we get pagination for free.
    paginate_by = 10
    context_object_name = 'artist_list'

    def __init__(self, **kwargs):
        super(InstrumentDetail, self).__init__(**kwargs)
        self.instrument_from_url = None

    def get_instrument_from_url(self):
        if not self.instrument_from_url:
            slug = self.kwargs['slug']
            self.instrument_from_url = get_object_or_404(Instrument, slug=slug)
        return self.instrument_from_url

    def get_queryset(self):
        instrument = self.get_instrument_from_url()
        return Artist.objects.filter(performance__instrument=instrument).distinct()

    def get_context_data(self, **kwargs):
        instrument = self.get_instrument_from_url()
        context_data = super(InstrumentDetail, self).get_context_data(**kwargs)
        context_data.update({
            'instrument': instrument,
        })
        return context_data

class ArtistDetail(DetailView):
    model = Artist

class ArtistList(ListView):
    model = Artist
    paginate_by = 10

class VenueDetail(ListView):
    # Making this a ListView so that we get pagination for free.
    paginate_by = 10
    context_object_name = 'concert_list'
    template_name = 'rasikapriya/venue_detail.html'

    def __init__(self, **kwargs):
        super(VenueDetail, self).__init__(**kwargs)
        self.venue_from_url = None

    def get_venue_from_url(self):
        if not self.venue_from_url:
            slug = self.kwargs['slug']
            self.venue_from_url = get_object_or_404(Venue, slug=slug)
        return self.venue_from_url

    def get_queryset(self):
        venue = self.get_venue_from_url()
        return venue.concert_set.all()

    def get_context_data(self, **kwargs):
        venue = self.get_venue_from_url()
        context_data = super(VenueDetail, self).get_context_data(**kwargs)
        context_data.update({
            'venue': venue,
        })
        return context_data
