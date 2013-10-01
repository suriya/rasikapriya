
from django.contrib import admin
from .models import Instrument, Artist

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
