from rest_framework import serializers
from notes.models import Note


class NoteSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(required=True, max_length=200)
    description = serializers.CharField(style={'base_template': 'textarea.html'})
    is_active = serializers.BooleanField(default=True)
    created_by = serializers.StringRelatedField()
    # created_by = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, null=True, blank=True)


    def create(self, validated_data):
        """Create a note (Note object) using the given validated data."""
        return NoteSerializer.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        """
        Update a note using the given validated data.
        """
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.is_active = validated_data.get('is_active', instance.is_active)
        instance.save()
        return instance

