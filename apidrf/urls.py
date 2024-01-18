from django.urls import include, path

from rest_framework.routers import DefaultRouter

from apidrf import views


router = DefaultRouter()
router.register(r'notes', views.NoteViewSet, basename='note')
router.register(r'users', views.UserViewSet, basename='user')


urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
]

