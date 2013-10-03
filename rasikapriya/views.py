
from django.views.generic import DetailView, ListView
from .models import Concert

class ConcertDetailView(DetailView):
    model = Concert
    context_object_name = 'concert'

class ConcertListView(ListView):
    model = Concert
    paginate_by = 10
    context_object_name = 'concert_list'
