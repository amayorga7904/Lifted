from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('posts/', views.all_posts, name='index'),
    path('posts/<int:user_id>/', views.your_posts, name='your_posts'),
    path('accounts/signup/', views.signup, name='signup'),
]