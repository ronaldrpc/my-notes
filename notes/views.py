from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from .models import Note

# Create your views here.

def home(request):
    notes = Note.objects.all().order_by('-last_modified_date')
    context = {'notes': notes}
    return render(request, 'notes/index.html', context)

def detail(request, note_id):
    note = get_object_or_404(Note, pk=note_id)
    return render(request, 'notes/detail.html', {'note': note})

def update(request, note_id):
    note = get_object_or_404(Note, pk=note_id)
    note.title = request.POST.get('title') or note.title
    note.description = request.POST.get('description') or note.description
    note.save()
    return HttpResponseRedirect(reverse('notes:detail', args=(note.id,)))
