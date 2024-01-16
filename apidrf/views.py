
from rest_framework import generics

from apidrf.serializers import NoteSerializer
from notes.models import Note


class NoteList(generics.ListCreateAPIView):
    """List all notes or create new ones."""
    queryset = Note.objects.all()
    serializer_class = NoteSerializer



class NoteDetail(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update or delete a note."""
    queryset = Note.objects.all()
    serializer_class = NoteSerializer



