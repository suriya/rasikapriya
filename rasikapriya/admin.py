
from django import forms
from django.contrib import admin
from .models import Instrument, Artist, Venue, Organization, Festival
from .widgets import PlacesAutocompleteWidget

admin.site.register(Instrument)
admin.site.register(Organization)
admin.site.register(Festival)

class ArtistAdmin(admin.ModelAdmin):
    filter_horizontal = ('instruments', )
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
