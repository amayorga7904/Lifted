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
    path('posts/detail/<int:post_id>/', views.posts_detail, name='detail'),
    path('posts/<int:post_id>/add_photo/', views.add_photo, name='add_photo'),
    path('posts/<int:post_id>/add_comment/', views.add_comment, name='add_comment'),
    path('post/delete/<int:pk>/', PostDelete.as_view(), name='post_delete'),
    path('post/update/<int:pk>/', views.PostUpdate.as_view(), name='posts_update'),
]