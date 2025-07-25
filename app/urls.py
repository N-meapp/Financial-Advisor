from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # adjust 'index' to your view name
    path('register/', views.register_view, name='register'), 
    path('blog/', views.blog, name='blog'), 
    path('investor/', views.investor, name='investor'), 
    path('contact/', views.contact, name='contact'), 
    path('login/', views.login, name='login'), 
    path('logout/', views.logout, name='logout'), 
    path('dia/', views.submit_financial_form, name='dia'), 
    path('generate-advice/<int:statement_id>/', views.generate_financial_advice, name='generate_financial_advice'),
    path('advice/', views.advice_history, name='advice_history'),
    


]
