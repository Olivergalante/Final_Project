from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from django.shortcuts import render
from .models import Post, Profile, Comment, User
from rest_framework import viewsets, generics
from .serializers import PostSerializer, ProfileSerializer, CommentSerializer, UserSearchSerializer


# Create your views here.

class UserSearchView(generics.ListAPIView):
    serializer_class = UserSearchSerializer

    def user_search(self, request):
        username = request.Get('username')
        if username:
            users = User.objects.filter(username__icontains=username)
            serializer = UserSearchSerializer(users, many=True)
            return Response(serializer.data)
        else:
            return Response(status=400)


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all().order_by('-created_at')
    serializer_class = CommentSerializer
