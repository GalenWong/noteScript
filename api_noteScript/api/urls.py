from django.urls import path

from . import views

urlpatterns = [
    path('uploads', views.upload_file, name='index'),
    path('transcribe', views.transcribe, name = 'main'),
]