from .models import Post, Profile, Comment, User
from rest_framework import viewsets
from .serializers import PostSerializer, ProfileSerializer, CommentSerializer, UserSerializer, CustomTokenObtainPairSerializer
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import make_password
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404


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
        user_id = self.request.data.get("user")

        # Check if the user ID is provided in the request data
        if user_id:
            # Try to get an existing user or create a new user if not found
            user, created = User.objects.get_or_create(id=user_id)

            # If the user is created, you might want to set additional user attributes
            if created:
                user.username = f"guest_{user_id}"  # Customize the username
                user.save()

            # Set the user and save the profile
            serializer.save(user=user)
        else:
            return Response(
                {"error": "User ID is required to update the profile."},
                status=status.HTTP_400_BAD_REQUEST,
            )


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all().order_by('-created_at')
    serializer_class = CommentSerializer

    @action(detail=True, methods=['POST'])
    def add_comment(self, request, pk=None):
        post = get_object_or_404(Post, pk=pk)
        serializer = CommentSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(post=post)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
