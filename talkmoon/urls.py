from django.urls import path
from . import views

urlpatterns = [
    path('', views.convert_image, name='convert_image'),
]