from django.urls import path
from . import views
from .views import PostListView
from .views import YourPostsListView
from .views import PostDelete


urlpatterns = [
    path('', views.home, name='home'),
    path('posts/', PostListView.as_view(), name='index'),
    path('posts/<int:user_id>/', YourPostsListView.as_view(), name='your_posts'),
    # path('posts/<int:user_id>/', views.your_posts, name='your_posts'),
    path('accounts/signup/', views.signup, name='signup'),
    path('post/create/', views.PostCreate.as_view(), name='post_create'),
    path('post/delete/<int:pk>/', PostDelete.as_view(), name='post_delete'),
]