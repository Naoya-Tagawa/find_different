from django.contrib import admin
from django.urls import path,include
from . import views
urlpatterns = [
    path("", views.index,name='index'),
    path('preview/<int:image_id>/', views.preview, name='preview'),
    path('transform/<int:image_id>/', views.transform, name='transform'),
    path('home/<image_id>/', views.home, name='home'),
    path("find", views.input_form,name='input'),
    path("find/output", views.output_form,name='output'),
    path("delete/<int:image_id>/", views.delete,name='delete'),
]
#1urlに対して1関数まで！