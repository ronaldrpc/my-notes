from django.urls import path, re_path
from . import views

app_name = 'notes'
urlpatterns = [
    path('', views.IndexView.as_view(), name="index"),
    re_path('(?:(?P<status>[a-zA-Z]+))?/$', views.IndexView.as_view(), name="index_archived"),  # Optional kwarg
    path('<int:pk>/', views.DetailView.as_view(), name="detail"),
    path('<int:note_id>/update/', views.update, name="update"),
    path('create/', views.create, name="create"),
    path('note/create/', views.NoteCreateView.as_view(), name="note-create"),
    path('note/<int:pk>/', views.NoteUpdateView.as_view(), name="note-update"),
]

