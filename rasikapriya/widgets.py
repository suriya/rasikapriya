
from django import forms
from django.utils.html import format_html

class PlacesAutocompleteWidget(forms.TextInput):
    class Media:
        js = ('https://maps.googleapis.com/maps/api/js?v=3.exp&sensor=false&libraries=places',
              'rasikapriya/js/places-autocomplete-widget.js',)
        css = {
            'all': ('rasikapriya/css/places-autocomplete-widget.css',),
        }

    def __init__(self, attrs=None):
        default_attrs = {
            'class': 'vTextField places-autocomplete-input',
        }
        if attrs:
            default_attrs.update(attrs)
        super(PlacesAutocompleteWidget, self).__init__(default_attrs)

    def render(self, name, value, attrs=None):
        id_input = ''
        if attrs:
            id_input = attrs.get('id', '')
        input_text = super(PlacesAutocompleteWidget, self).render(name, value, attrs)
        map_canvas = format_html(u'<div class="places-autocomplete-map-canvas places-autocomplete-corresponding-input-{0}"></div>', id_input)
        return format_html(u'<div class="places-autocomplete-container">{0}{1}</div>', input_text, map_canvas)
