from rest_framework.permissions import IsAuthenticated
from .models import Post, Profile, Comment
from rest_framework import viewsets
from .serializers import PostSerializer, ProfileSerializer, CommentSerializer, UserSerializer, CustomTokenObtainPairSerializer
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import make_password
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.decorators import action


# Create your views here.
class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            password = make_password(request.data['password'])
            user = serializer.save(password=password)
            Profile.objects.create(user=user)  # Create profile here
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    parser_classes = [MultiPartParser, FormParser]

    def get_queryset(self):
        return Post.objects.all().order_by('-created_at')


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    lookup_field = "user_id"

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all().order_by('-created_at')
    serializer_class = CommentSerializer


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class LoginView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer  # Use your custom serializer

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == status.HTTP_200_OK:
            # If login is successful, you can include additional information in the response
            user = request.user
            # Adjust this based on your profile serialization logic
            profile_serializer = ProfileSerializer(user.profile)
            response.data['profile'] = profile_serializer.data

        return response
