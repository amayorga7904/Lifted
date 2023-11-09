from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .mixins import UserCanDeletePostMixin, UserCanUpdatePostMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.list import ListView
from django.shortcuts import render, redirect
from .models import Post, Comment, Photo
from django.contrib.auth import login
from django.urls import reverse_lazy
from .forms import CommentForm
import getpass
import boto3
import uuid
import os
# Create your views here.

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


@login_required
def home(request):
  return render(request, 'home.html')


@login_required
def all_posts(request):
    posts = Post.objects.all()
    return render(request, 'posts/index.html', {'posts': posts})


@login_required
def posts_detail(request, post_id):
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
      user = form.save()
      login(request, user)
      return redirect('index')
    else:
      error_message = 'Invalid sign up - try again'
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)


def get_logged_in_username():
    username = getpass.getuser()
    return username


@login_required
def add_comment(request, post_id):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.user = request.user 
            new_comment.post_id = post_id
            new_comment.save()
    return redirect('detail', post_id=post_id)


@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    if comment.user == request.user:
        post_id = comment.post.id  
        comment.delete()
        return redirect('detail', post_id=post_id)
    else:
        return redirect('detail', post_id=comment.post.id) 
    


class PostCreate(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['description']
    template_name = 'main_app/post_form.html'
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        form.instance.user = self.request.user
        post = form.save(commit=False)
        post.save()
        image = self.request.FILES.get('photo-file', None) 
        if image:
            url = self.upload_image_to_s3(image)
            Photo.objects.create(url=url, post_id=post.id)
        return super().form_valid(form)
    def upload_image_to_s3(self, image_file):
        s3 = boto3.client('s3')
        key = uuid.uuid4().hex[:6] + image_file.name[image_file.name.rfind('.'):]
        try:
            bucket = os.environ['S3_BUCKET']
            s3.upload_fileobj(image_file, bucket, key)
            return f"{os.environ['S3_BASE_URL']}{bucket}/{key}"
        except Exception as e:
            print('An error occurred uploading file to S3')
            print(e)
            return None



class CommentCreate(LoginRequiredMixin, CreateView):
  model = Comment
  fields = '__all__'



class PostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'posts/index.html' 
    context_object_name = 'object_list'  



class YourPostsListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'posts/your_posts.html'  
    context_object_name = 'your_posts' 

    def get_queryset(self):
        return Post.objects.filter(user=self.request.user)



class PostDelete(UserCanDeletePostMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('index')



class PostUpdate(UserCanUpdatePostMixin, UpdateView):
    model = Post
    fields = ['description']
    success_url = reverse_lazy('index')
    template_name = 'main_app/post_form.html'
    def form_valid(self, form):
        form.instance.user = self.request.user
        post = form.save(commit=False)
        post.save()
        image = self.request.FILES.get('photo-file', None) 
        if image:
            url = self.upload_image_to_s3(image)
            Photo.objects.create(url=url, post_id=post.id)
        return super().form_valid(form)
    def upload_image_to_s3(self, image_file):
        s3 = boto3.client('s3')
        key = uuid.uuid4().hex[:6] + image_file.name[image_file.name.rfind('.'):]
        try:
            bucket = os.environ['S3_BUCKET']
            s3.upload_fileobj(image_file, bucket, key)
            return f"{os.environ['S3_BASE_URL']}{bucket}/{key}"
        except Exception as e:
            print('An error occurred uploading file to S3')
            print(e)
            return None



def custom_403_view(request):
    return render(request, '403.html', status=403)