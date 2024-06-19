from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_image, name='upload_image'),
    path('', views.upload_page, name='upload_page'),  # Default to upload page
]