from rest_framework import permissions


class IsCreatedBy(permissions.BasePermission):
    """Custom permission to only allow users to see the notes created by themselves."""
    
    def has_object_permission(self, request, view, obj):
        return obj.created_by == request.user

