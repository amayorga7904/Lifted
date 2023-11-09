from .views import YourPostsListView
from .views import PostListView
from .views import PostDelete
from django.urls import path
from . import views




urlpatterns = [
    path('', views.home, name='home'),
    path('accounts/signup/', views.signup, name='signup'),
    path('posts/', PostListView.as_view(), name='index'),
    path('post/create/', views.PostCreate.as_view(), name='post_create'),
    path('post/delete/<int:pk>/', PostDelete.as_view(), name='post_delete'),
    path('posts/<int:user_id>/', YourPostsListView.as_view(), name='your_posts'),
    path('post/update/<int:pk>/', views.PostUpdate.as_view(), name='posts_update'),
    path('comments/<int:comment_id>/delete/', views.delete_comment, name='comment_delete'),
    path('posts/<int:post_id>/add_comment/', views.add_comment, name='add_comment'),
    path('posts/<int:post_id>/add_photo/', views.add_photo, name='add_photo'),
    path('posts/detail/<int:post_id>/', views.posts_detail, name='detail'),
]
