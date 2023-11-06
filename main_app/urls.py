from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('allposts/', views.allposts, name='allposts'),
    path('yourposts/', views.yourposts, name='yourposts'),
    path('accounts/signup/', views.signup, name='signup'),
]