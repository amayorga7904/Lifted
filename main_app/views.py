import os
import uuid
import boto3
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .mixins import UserCanDeletePostMixin, UserCanUpdatePostMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Post, Comment, Photo
from django.views.generic.list import ListView
from .forms import CommentForm
import getpass
from django.contrib.auth.models import User
# Create your views here.




@login_required
def home(request):
  return render(request, 'home.html')

@login_required
def all_posts(request):
    posts = Post.objects.all()
    return render(request, 'posts/index.html', {'posts': posts})




@login_required
def posts_detail(request, post_id, user_id):
  post = Post.objects.get(id=post_id)
  user = User.objects.get(id=user_id)
  comment_form = CommentForm()
  return render(request, 'posts/detail.html', {
    'post': post, 'comment_form': comment_form, 'user': user
  })


def signup(request):
  error_message = ''
  if request.method == 'POST':
    form = UserCreationForm(request.POST)
    if form.is_valid():
      # Save the user to the db
      user = form.save()
      # Automatically log in the new user
      login(request, user)
      return redirect('index')
    else:
      error_message = 'Invalid sign up - try again'
  # A bad POST or a GET request, so render signup template
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)


class PostCreate(LoginRequiredMixin, CreateView):
  model = Post
  fields = ['description']
  success_url = reverse_lazy('index')

  def form_valid(self, form):
      form.instance.user = self.request.user

      # Create a Post object for the 'index' page
      post_for_index = form.save(commit=False)
      post_for_index.save()

      # Create a Post object for the 'your_posts' page
      post_for_your_posts = form.save(commit=False)
      post_for_your_posts.save()

      return super().form_valid(form)

@login_required
def add_photo(request, post_id):
  photo_file = request.FILES.get('photo-file', None)
  if photo_file:
    s3 = boto3.client('s3')
    key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
    try:
      bucket = os.environ['S3_BUCKET']
      s3.upload_fileobj(photo_file, bucket, key)
      url = f"{os.environ['S3_BASE_URL']}{bucket}/{key}"
      Photo.objects.create(url=url, post_id=post_id)
    except Exception as e:
      print('An error occurred uploading file to S3')
      print(e)
  return redirect('detail', post_id=post_id)


class CommentCreate(LoginRequiredMixin, CreateView):
  model = Comment
  fields = '__all__'

class PostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'posts/index.html'  # Specify the template to be used
    context_object_name = 'object_list'  # Context variable to access the list of objects in the template


class YourPostsListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'posts/your_posts.html'  # Specify the template to be used
    context_object_name = 'your_posts'  # Context variable to access the list of your posts

    def get_queryset(self):
        # Filter the posts by the currently logged-in user
        return Post.objects.filter(user=self.request.user)

class PostDelete(UserCanDeletePostMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('index')


class PostUpdate(UserCanUpdatePostMixin, UpdateView):
  model = Post
  fields = ['description']
  success_url = reverse_lazy('index')

def get_logged_in_username():
    username = getpass.getuser()
    return username

@login_required
def add_comment(request, post_id):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.user = request.user  # Set the user to the currently logged-in user
            new_comment.post_id = post_id
            new_comment.save()
            
    return redirect('detail', post_id=post_id)

@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    
    if comment.user == request.user:
        post_id = comment.post.id  # Get the post ID before deleting the comment
        comment.delete()
        # Redirect to the post detail page with the correct post_id
        return redirect('detail', post_id=post_id)
    else:
        # Handle the case where the user doesn't have permission (you can customize this)
        return redirect('detail', post_id=comment.post.id)  # Redirect to the post detail page
