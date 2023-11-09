from django.db import models
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
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
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField(max_length=350)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    # username = models.CharField(max_length=100)
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
