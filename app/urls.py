from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # adjust 'index' to your view name
    path('register/', views.register, name='register'), 
]
