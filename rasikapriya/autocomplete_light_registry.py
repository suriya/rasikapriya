
import autocomplete_light
from .models import Venue, Instrument, Artist

autocomplete_light.register(Venue,
    search_fields=('name', 'address',),
    autocomplete_js_attributes={'placeholder': 'Venue name ...'})

autocomplete_light.register(Artist,
    search_fields=('native_place', 'initials', 'first_name', 'middle_name', 'last_name',),

    autocomplete_js_attributes={'placeholder': 'Artist name ...'})

autocomplete_light.register(Instrument,
    search_fields=('name',),
    autocomplete_js_attributes={
        'placeholder': 'Instrument name ...',
        'minimum_characters': 0,
    })
