from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from django.shortcuts import render
from .models import Post, Profile
from rest_framework import viewsets, status
from .serializers import PostSerializer, ProfileSerializer


# Create your views here.
