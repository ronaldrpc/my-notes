from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic

from .models import Note

class IndexView(generic.ListView):
    template_name = 'notes/index.html'
    context_object_name = 'notes'

    def get_queryset(self):
        return Note.objects.all().order_by('-last_modified_date')


class DetailView(generic.DetailView):
    model = Note
    template_name = 'notes/detail.html'


def update(request, note_id):
    note = get_object_or_404(Note, pk=note_id)
    note.title = request.POST.get('title') or note.title
    note.description = request.POST.get('description') or note.description
    note.save()
    return HttpResponseRedirect(reverse('notes:detail', args=(note.id,)))
