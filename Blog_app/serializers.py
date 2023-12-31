from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import Post, Profile, Comment, User
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id', 'user', 'bio', 'location', 'birth_date']
        lookup_field = "user_id"  # Keep it consistent with the view


class PostSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False, use_url=True)

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'author',
                  'image', 'created_at', 'username']


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'password', 'profile']


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'author', 'post', 'body', 'created_at']

    def create(self, validated_data):
        # Set the author based on the logged-in user if authenticated
        user = self.context['request'].user
        if user.is_authenticated:
            validated_data['author'] = user

        # Set the post based on the post ID in the URL
        post_id = self.context['view'].kwargs.get('post_id')
        validated_data['post'] = get_object_or_404(Post, pk=post_id)

        return super().create(validated_data)


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'}, trim_whitespace=False)
    remember = serializers.BooleanField(required=False, default=False)


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        print(self)
        data["userId"] = self.user.id
        return data
