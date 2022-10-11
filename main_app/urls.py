from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('cats/', views.cats_index, name='cats_index'),
    path('cats/<int:cat_id>/', views.cats_detail, name='cats_detail'),
    path('cats/create/', views.CatsCreate.as_view(), name='cats_create'),
    path('cats/<int:pk>/update/', views.CatsUpdate.as_view(), name='cats_update'),
    path('cats/<int:pk>/delete/', views.CatsDelete.as_view(), name='cats_delete'),
    path('cats/<int:cat_id>/add_feeding/', views.add_feeding, name='add_feeding'),
    path('toy/create/', views.ToysCreate.as_view(), name='toys_create'),
    path('toys/', views.ToysIndex.as_view(), name='toys_index'),
    path('toys/<int:pk>/', views.ToysDetail.as_view(), name='toys_detail'),
    path('toys/<int:pk>/update/', views.ToysUpdate.as_view(), name='toys_update'),
    path('toys/<int:pk>/delete/', views.ToysDelete.as_view(), name='toys_delete'),
]

