from rest_framework.decorators import api_view, permission_classes, throttle_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.pagination import PageNumberPagination
from rest_framework.throttling import UserRateThrottle
from django.db.models import Q

from users.models import FriendRequest, User

from .serializers import (
    FriendRequestResponseSerializer,
    FriendRequestSerializer,
    ListRequestSerializer,
    TokenSerializer,
    UserSerializer,
)


# Set throttle_classes to FriendRequestThrottle to limit the number of requests to this endpoint.
class FriendRequestThrottle(UserRateThrottle):
    scope = "friend-request"  # defined in settings.py


@api_view(["POST"])
@permission_classes([AllowAny])
def signup(request: Request) -> Response:
    """
    Create a new user account.
    """
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(
            {"message": "User created successfully"}, status=status.HTTP_201_CREATED
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes([AllowAny])
def login(request: Request) -> Response:
    """
    Login a user.
    """
    serializer = TokenSerializer(data=request.data, context={"request": request})
    if serializer.is_valid():
        data = serializer.generate_token(validated_data=serializer.validated_data)
        return Response(data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def search(request: Request, query: str) -> Response:
    """
    Search for a user by email or name (case-insensitive) with pagination.
    """
    users = User.objects.filter(Q(email__iexact=query) | Q(name__icontains=query))

    paginator = PageNumberPagination()
    paginator.page_size = 10  # 10 users per page
    result_page = paginator.paginate_queryset(users, request)

    serializer = UserSerializer(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
@throttle_classes([FriendRequestThrottle])
def send_friend_request(request: Request) -> Response:
    """
    Send a friend request to another user. (Rate limited: 3 requests per minute)
    """
    serializer = FriendRequestSerializer(
        data=request.data, context={"request": request}
    )
    if serializer.is_valid():
        friend_request: FriendRequest = serializer.send_request(
            validated_data=serializer.validated_data
        )
        return Response(
            {"request_id": friend_request.pk, "message": "Friend request sent"},
            status=status.HTTP_201_CREATED,
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def respond_friend_request(request: Request) -> Response:
    """
    Accept or reject a friend request.
    """
    serializer = FriendRequestResponseSerializer(
        data=request.data, context={"request": request}
    )
    if serializer.is_valid():
        message: str = serializer.respond_request(
            validated_data=serializer.validated_data
        )
        return Response({"message": message}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def friends_list(request: Request) -> Response:
    """
    Get a list of friends.
    """
    serializer = ListRequestSerializer(context={"request": request})
    data: list = serializer.get_friends()
    return Response(data, status=status.HTTP_200_OK)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def friend_requests(request: Request) -> Response:
    """
    Get a list of pending friend requests.
    """
    serializer = ListRequestSerializer(context={"request": request})
    data: list = serializer.get_pending_requests()
    return Response(data, status=status.HTTP_200_OK)
