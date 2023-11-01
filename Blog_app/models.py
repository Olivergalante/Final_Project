from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Image(models.Model):
    image = models.ImageField(upload_to='images/')
    image_name = models.CharField(max_length=100)
    image_caption = models.TextField(max_length=350)
    image_likes = models.IntegerField(default=0)
    image_comments = models.IntegerField(default=0)
    image_author = models.ForeignKey(User, on_delete=models.CASCADE)
    image_created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.image_name


class Profile(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.user_id)


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField(max_length=350)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="comments")
    body = models.TextField(max_length=350)
    created_at = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="comments")

    def __str__(self):
        return f"{self.author.username}: {self.body[:50]}"
