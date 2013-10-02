
import autocomplete_light
from django import forms
from django.contrib import admin
from .models import (Instrument, Artist, Venue, Organization, Festival,
        Concert, Performance)
from .widgets import PlacesAutocompleteWidget

class VenueForm(forms.ModelForm):
    class Meta:
        model = Venue
        widgets = {
            'address': PlacesAutocompleteWidget(),
        }
class VenueAdmin(admin.ModelAdmin):
    form = VenueForm
admin.site.register(Venue, VenueAdmin)

# admin.site.register(Instrument)
# admin.site.register(Organization)
# admin.site.register(Festival)

# class ArtistAdmin(admin.ModelAdmin):
#     filter_horizontal = ('instruments', )
# admin.site.register(Artist, ArtistAdmin)

# class ArtistInline(admin.TabularInline):
#     form = autocomplete_light.modelform_factory(Artist)
#     model = Artist
class ArtistAdmin(admin.ModelAdmin):
    form = autocomplete_light.modelform_factory(Artist)
#     inlines = [ArtistInline]
admin.site.register(Artist, ArtistAdmin)

class OrganizationAdmin(admin.ModelAdmin):
    form = autocomplete_light.modelform_factory(Organization)
admin.site.register(Organization, OrganizationAdmin)

class FestivalAdmin(admin.ModelAdmin):
    form = autocomplete_light.modelform_factory(Festival)
admin.site.register(Festival, FestivalAdmin)

class PerformanceInline(admin.TabularInline):
    form = autocomplete_light.modelform_factory(Performance)
    model = Performance
#     extra = 4
class ConcertAdmin(admin.ModelAdmin):
    form = autocomplete_light.modelform_factory(Concert)
    inlines = (PerformanceInline,)
admin.site.register(Concert, ConcertAdmin)
# admin.site.register(Concert)
