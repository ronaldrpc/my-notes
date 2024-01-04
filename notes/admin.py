from django.contrib import admin
from .models import Note


class NoteAdmin(admin.ModelAdmin):
    fields = ['title', 'description']
    list_display = ['title', 'description', 'create_date', 'last_modified_date']
    list_filter = ['last_modified_date']
    search_fields = ['title']

admin.site.register(Note, NoteAdmin)
