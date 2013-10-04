
from django.views.generic import DetailView, ListView
from .models import Concert, Artist, Instrument
from django.shortcuts import get_object_or_404

class ConcertDetailView(DetailView):
    model = Concert
    context_object_name = 'concert'

class ConcertListView(ListView):
    model = Concert
    paginate_by = 10
    context_object_name = 'concert_list'

class InstrumentDetailView(ListView):
    # Making this a ListView so that we get pagination for free.
    paginate_by = 10
    context_object_name = 'artist_list'

    def __init__(self, **kwargs):
        super(InstrumentDetailView, self).__init__(**kwargs)
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
        context_data = super(InstrumentDetailView, self).get_context_data(**kwargs)
        context_data.update({
            'instrument': instrument,
        })
        return context_data

class ArtistDetailView(DetailView):
    model = Artist
