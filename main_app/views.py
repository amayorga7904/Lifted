import os
import uuid
import boto3
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Post, Comment, Photo
from .forms import CommentForm
# Create your views here.

def home(request):
  return render(request, 'home.html')

def all_posts(request):
    posts = Post.objects.all()
    return render(request, 'posts/index.html', {'posts': posts})


def your_posts(request, user_id):
    # Your view logic here
    posts = Post.objects.filter(user_id=user_id)
    return render(request, 'posts/your_posts.html', {'your_posts': posts})


def posts_details(request, post_id):
  post = Post.objects.get(id=post_id)
  comment_form = CommentForm()
  return render(request, 'posts/detail.html', {
    'post': post, 'comment_form': comment_form
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

  def form_valid(self, form):
      form.instance.user = self.request.user
      return super().form_valid(form)

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


class PostDelete(LoginRequiredMixin, DeleteView):
  model = Post
  success_url = '/posts'


def add_comment(request, post_id):
  form = CommentForm(request.POST)
  if form.is_valid():
    new_comment = form.save(commit=False)
    new_comment.post_id = post_id
    new_comment.save()
  return redirect('detail', post_id=post_id)