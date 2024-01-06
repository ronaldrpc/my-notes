from django.db import models
from django.urls import reverse


class Note(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField("Description")
    create_date = models.DateTimeField(auto_now_add=True)
    last_modified_date = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)


    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("notes:note-update", kwargs={"pk": self.pk})
