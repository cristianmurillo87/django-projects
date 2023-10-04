from django.contrib.auth.hashers import make_password
from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from backend.permissions import IsUserOrReadOnly

from .models import User
from .serializers import (
    CustomTokenObtainPairSerializer,
    SearchSerializer,
    UserSerializer,
)


class CustomTokenObtainPairViewSerializer(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsUserOrReadOnly]
    lookup_field = "username"
    lookup_url_kwarg = "username"


@api_view(["GET"])
def search(request: Request):
    query = request.query_params.get("query", None)
    if query is not None:
        users = User.objects.filter(username__contains=query)
        serializer = SearchSerializer(users, many=True)
        return Response(dict(users=serializer.data))
    return Response(dict(users=[]))


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def register(request: Request):
    data = request.data
    try:
        user = User.objects.create(
            username=data["username"],
            email=data["email"],
            password=make_password(data["password"]),
        )
    except Exception:
        message = dict(detail="Something went wrong")
        return Response(message, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def follow(request: Request, username: str):
    me = request.user
    user = User.objects.get(username=username)
    if not user:
        message = dict(message="User not found")
        return Response(message, status=status.HTTP_400_BAD_REQUEST)
    if user in me.following.all():
        me.following.remove(user)
        return Response({"detail": "Unfollowed"}, status=status.HTTP_200_OK)
    else:
        me.following.add(user)
        return Response({"detail": "Followed"}, status=status.HTTP_200_OK)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def reco(request):
    """Returns 5 first found non-followed users for the current user"""
    users = User.objects.exclude(username=request.user.username)
    users = users.exclude(id__in=request.user.following.all())[:5]
    serializer = SearchSerializer(users, many=True)
    return Response(serializer.data)
