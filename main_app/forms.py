from django.forms import ModelForm
from .models import Comment
from .models import Image
from django import forms  # Replace MyModel with your actual model name

class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['image', 'description']

class CommentForm(ModelForm):
  class Meta:
    model = Comment
    fields = ['content']