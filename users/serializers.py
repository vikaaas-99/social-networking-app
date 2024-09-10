from rest_framework import serializers
from rest_framework.request import Request
from rest_framework_simplejwt.tokens import RefreshToken

from .models import FriendRequest, User


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer to create a new user account.
    """

    class Meta:
        model = User
        fields = ("id", "email", "name", "password")

    def create(self, validated_data: dict) -> User:
        user = User(email=validated_data["email"])
        user.set_password(validated_data["password"])
        user.save()
        return user


class TokenSerializer(serializers.Serializer):
    """
    Serializer to login a user and generate a token.
    """

    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data: dict[str, str]) -> dict:
        """
        Validate the email and password.
        """
        email = data["email"].lower()
        password = data["password"]

        user = User.objects.filter(email=email).first()
        if not user:
            raise serializers.ValidationError("User not found with this email")
        if not user.check_password(password):
            raise serializers.ValidationError("Incorrect password")
        data["user"] = user
        return data

    def generate_token(self, validated_data: dict) -> str:
        """
        Generate a token for the user.
        """
        user = validated_data["user"]

        refresh = RefreshToken.for_user(user)
        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }


class FriendRequestSerializer(serializers.Serializer):
    """
    Serializer to send a friend request.
    """

    receiver_id = serializers.IntegerField()

    def validate(self, data: dict) -> User:
        """
        Validate the receiver ID.
        """
        request: Request = self.context["request"]
        user = request.user
        receiver_id = data["receiver_id"]

        receiver = User.objects.filter(id=receiver_id).first()
        if not receiver:
            raise serializers.ValidationError("User not found with this ID")
        if receiver == user:
            raise serializers.ValidationError(
                "You cannot send a friend request to yourself"
            )
        if FriendRequest.objects.filter(sender=user, receiver=receiver).exists():
            raise serializers.ValidationError(
                "Friend request already sent to this user"
            )
        data["receiver"] = receiver
        return data

    def send_request(self, validated_data: dict) -> FriendRequest:
        """
        Send a friend request to the receiver.
        """
        request: Request = self.context["request"]
        user = request.user
        receiver: User = validated_data["receiver"]

        friend_request = FriendRequest.objects.create(sender=user, receiver=receiver)
        return friend_request


class FriendRequestResponseSerializer(serializers.Serializer):
    """
    Serializer to respond to a friend request. (accept or reject)
    """

    request_id = serializers.IntegerField()
    action = serializers.ChoiceField(choices=["accept", "reject"])

    def validate(self, data: dict) -> FriendRequest:
        """
        Validate the friend request ID and action.
        """
        request: Request = self.context["request"]
        user = request.user
        # print(user)
        request_id = data["request_id"]

        friend_request = FriendRequest.objects.filter(pk=request_id).first()
        if not friend_request:
            raise serializers.ValidationError("Friend request not found with this ID")
        if friend_request.receiver != user:
            raise serializers.ValidationError(
                "You cannot respond to this friend request"
            )
        if friend_request.status != "pending":
            raise serializers.ValidationError(
                "This friend request is already responded"
            )
        data["friend_request"] = friend_request
        return data

    def respond_request(self, validated_data: dict) -> str:
        """
        Accept or reject the friend request.
        """
        friend_request: FriendRequest = validated_data["friend_request"]
        action = validated_data["action"]

        if action == "accept":
            message = "Friend request accepted"
            friend_request.status = "accepted"
        else:
            message = "Friend request rejected"
            friend_request.status = "rejected"
        friend_request.save()
        return message


class ListRequestSerializer(serializers.Serializer):
    """
    Serializer to get a list of friends and pending friend requests.
    """

    def get_friends(self) -> list[dict]:
        """
        Get a list of friends.
        """
        request: Request = self.context["request"]
        user = request.user

        friends = FriendRequest.objects.filter(
            sender=user, status="accepted"
        ) | FriendRequest.objects.filter(receiver=user, status="accepted")
        friends_list = []
        for friend in friends:
            if friend.sender == user:
                friends_list.append(friend.receiver)
            else:
                friends_list.append(friend.sender)
        serializer = UserSerializer(friends_list, many=True)
        return serializer.data

    def get_pending_requests(self) -> list[dict]:
        """
        Get a list of pending friend requests.
        """
        request: Request = self.context["request"]
        user = request.user

        pending_requests = FriendRequest.objects.filter(receiver=user, status="pending")
        pending_requests = [request.sender for request in pending_requests]
        serializer = UserSerializer(pending_requests, many=True)
        return serializer.data
