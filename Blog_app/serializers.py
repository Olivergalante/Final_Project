from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import Post, Profile, Comment, User


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id', 'user_id', 'user']


class PostSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='author.username')
    image_url = serializers.ImageField(required=False)

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'author',
                  'created_at', 'username', 'image_url']


class UserSerializer(serializers.ModelSerializer):
    print("USER SERIALIZER")

    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'password']
        profile = ProfileSerializer()


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'body', 'post', 'author', 'created_at']


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
        # data["username"] = self.user.username
        # data["name"] = self.user.first_name + " " + self.user.last_name
        return data
