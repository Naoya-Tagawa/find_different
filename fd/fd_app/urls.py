from django.contrib import admin
from django.urls import path,include
from . import views
urlpatterns = [
    path("", views.index,name='index'),
    path('preview/<int:image_id>/', views.preview, name='preview'),
    path('transform/<int:image_id>/', views.transform, name='transform'),
]