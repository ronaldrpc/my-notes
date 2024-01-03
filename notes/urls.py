from django.urls import path
from . import views

app_name = 'notes'
urlpatterns = [
    path('', views.home, name="index"),
    path('<int:note_id>/', views.detail, name="detail"),
]

