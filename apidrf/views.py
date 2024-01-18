from django.contrib.auth.models import User

from rest_framework import permissions, viewsets

from apidrf.permissions import IsCreatedBy
from apidrf.serializers import NoteSerializer, UserSerializer
from notes.models import Note


class NoteViewSet(viewsets.ModelViewSet):
    """
    This viewset provides list, create, retrieve, update and delete operations.
    """

    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    permission_classes = [permissions.IsAuthenticated, IsCreatedBy]

    def perform_create(self, serializer):
        self.set_created_by(serializer)
    
    def set_created_by(self, serializer):
        """Set created_by field using logged in user."""
        serializer.save(created_by=self.request.user)

    def get_queryset(self):
        """
        Be careful, this overrided method is shared by all actions (list, retrieve, update, etc)
        It can yield weird (different) outcomes than expected. For example:
        
        Raise 404 status code rather than 403.
        """
        filtered_notes = Note.objects.filter(created_by=self.request.user)
        return filtered_notes.order_by('-last_modified_date')


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """This viewset provides list and retrieve actions."""
    queryset = User.objects.all()
    serializer_class = UserSerializer


