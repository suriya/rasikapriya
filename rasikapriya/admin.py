
from django import forms
from django.contrib import admin
from .models import Instrument, Artist, Venue
from .widgets import PlacesAutocompleteWidget

admin.site.register(Instrument)

class ArtistAdmin(admin.ModelAdmin):
    filter_horizontal = ('instruments', )
#     fields = (
#         ('native_place', 'initials', 'first_name', 'middle_name', 'last_name', ),
#         'instruments',
#         'home_page',
#         'description',
#     )

admin.site.register(Artist, ArtistAdmin)

class VenueForm(forms.ModelForm):
    class Meta:
        model = Venue
        widgets = {
            'address': PlacesAutocompleteWidget(),
        }

class VenueAdmin(admin.ModelAdmin):
    form = VenueForm
admin.site.register(Venue, VenueAdmin)
