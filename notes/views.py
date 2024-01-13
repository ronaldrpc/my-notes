from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
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
        active_user_notes = Note.objects.filter(is_active=active_status, created_by=self.request.user)
        ordered_notes = active_user_notes.order_by('-last_modified_date')
        return ordered_notes


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

    def form_valid(self, form):
        """
        Override this method in order to set the logged user to the instance related to the form.
        This instance is the object (Note) that will be saved using the form data.
        """
        form.instance.created_by = self.request.user
        form.instance.is_active = True  # El default True dejó de funcionar desde que agregue el 'created_by'
        return super(NoteCreateView, self).form_valid(form)
    

class NoteUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Note
    form_class = NoteForm
    template_name = 'notes/detail.html'

    def test_func(self):
        """Check if the current object (Note) was created by the logged user."""
        logged_user = self.request.user
        current_note = self.get_object()
        return current_note.created_by == logged_user




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