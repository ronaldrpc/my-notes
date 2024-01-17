from django.contrib.auth.models import User

from rest_framework import serializers

from notes.models import Note


class NoteSerializer(serializers.ModelSerializer):
    created_by = serializers.ReadOnlyField(source="created_by.username")

    class Meta:
        model = Note
        fields = ['id', 'title', 'description', 'is_active', 'created_by', 'create_date', 'last_modified_date']

class UserSerializer(serializers.ModelSerializer):
    note_set = serializers.PrimaryKeyRelatedField(many=True, queryset=Note.objects.all())

    class Meta:
        model = User
        fields = ['id', 'username', 'note_set']
