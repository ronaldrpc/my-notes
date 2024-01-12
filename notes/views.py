from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from .forms import NoteForm
from .models import Note

class IndexView(LoginRequiredMixin, generic.ListView):
    context_object_name = 'notes'
    template_name = 'notes/index.html'

    def get_queryset(self):
        active_status = True
        kw_status = self.kwargs.get('status')
        if kw_status and kw_status == 'archived':
            active_status = False
        notes = Note.objects.all().filter(is_active=active_status).order_by('-last_modified_date')
        return notes


class DetailView(LoginRequiredMixin, generic.DetailView):
    model = Note
    template_name = 'notes/detail.html'
    login_url = reverse_lazy('notes:login')


def update(request, note_id):
    note = get_object_or_404(Note, pk=note_id)
    note.title = request.POST.get('title') or note.title
    note.description = request.POST.get('description') or note.description
    note.save()
    return HttpResponseRedirect(reverse('notes:detail', args=(note.id,)))

def create(request):
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save()
            return HttpResponseRedirect(reverse('notes:detail', args=(note.id,)))
    else:
        form = NoteForm()
    return render(request, 'notes/create.html', {'form': form})



## Form handling with class-based views

class NoteCreateView(LoginRequiredMixin, CreateView):
    model = Note
    form_class = NoteForm
    template_name = 'notes/create.html'

    # 'Models and request.user' page 424
    
class NoteUpdateView(LoginRequiredMixin, UpdateView):
    model = Note
    form_class = NoteForm
    template_name = 'notes/detail.html'




## Handling authentication (Move it to another app?)
class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        next_url = self.request.POST.get('next', )
        if next_url:
            return next_url
        return reverse_lazy('notes:index')
## 