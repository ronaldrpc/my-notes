from django.urls import path
from apidrf import views


urlpatterns = [
    path('notes/', views.notes_list_create),
    path('notes/<int:pk>/', views.notes_detail),
]


