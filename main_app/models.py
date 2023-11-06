from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Post(models.Model):
    url = models.CharField(max_length=200)
    description = models.TextField(max_length=250)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Photo by user_id: {self.user.id} @{self.url}"


    class Meta:
        ordering = ['-created_at']



class Comment(models.Model):
    content = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)  
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return f"Comment by user_id: {self.user.id} on post_id: {self.post.id}"
