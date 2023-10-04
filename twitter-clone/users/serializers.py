from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import User


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user: User):
        token = super().get_token(user)
        token["username"] = user.username
        token["avatar"] = user.avatar.url
        return token


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "email", "password"]


class UserSerializer(serializers.ModelSerializer):
    email = serializers.ReadOnlyField()
    username = serializers.ReadOnlyField()
    followers = serializers.SerializerMethodField(read_only=True)
    i_follow = serializers.SerializerMethodField(read_only=True)
    following = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "avatar",
            "bio",
            "cover_image",
            "date_joined",
            "i_follow",
            "followers",
            "following",
            "name",
        ]

    # The tree following methods are defined because of the three fields
    # whose serializer type is SerializerMethodField. In this case,
    # the functions must have the following structure:
    # get_"field_name"
    def get_i_follow(self, obj):
        current_user = self.context.get("request").user
        return current_user in obj.followed.all()

    def get_followers(self, obj):
        return obj.followed.count()

    def get_following(self, obj):
        return obj.following.count()


class SearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "avatar"]
