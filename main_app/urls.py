from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    # add another url path to 'about/'
    path('about/', views.about),
    path('cats/', views.cats_index),
    path('cats/<int:cat_id>/', views.cats_detail, name='detail')
]

