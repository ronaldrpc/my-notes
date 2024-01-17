from django.contrib.auth.models import User

from rest_framework import generics, permissions

from apidrf.serializers import NoteSerializer, UserSerializer
from notes.models import Note


class NoteList(generics.ListCreateAPIView):
    """List all notes or create new ones."""
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        self.set_created_by(serializer)
    
    def set_created_by(self, serializer):
        """Set created_by field using logged in user."""
        serializer.save(created_by=self.request.user)


class NoteDetail(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update or delete a note."""
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    permission_classes = [permissions.IsAuthenticated]


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

