from django.shortcuts import get_object_or_404, render
from .models import Note

# Create your views here.

def home(request):
    notes = Note.objects.all().order_by('-last_modified_date')
    context = {'notes': notes}
    return render(request, 'notes/index.html', context)

def detail(request, note_id):
    note = get_object_or_404(Note, pk=note_id)
    return render(request, 'notes/detail.html', {'note': note})
