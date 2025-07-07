from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # adjust 'index' to your view name
    path('register/', views.register, name='register'), 
    path('blog/', views.blog, name='blog'), 
    path('investor/', views.investor, name='investor'), 
    path('contact/', views.contact, name='contact'), 



]
