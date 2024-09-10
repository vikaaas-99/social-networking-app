from django.urls import path
from .views import *


urlpatterns = [
    path("signup/", signup, name="signup"),  # Endpoint to create a new user account
    path("login/", login, name="login"),  # Endpoint to login a user
    path(
        "search/<str:query>/", search, name="search"
    ),  # Endpoint to search for a user by email or name
    path(
        "send-request/", send_friend_request, name="send-request"
    ),  # Endpoint to send a friend request
    path(
        "respond-request/", respond_friend_request, name="respond-request"
    ),  # Endpoint to respond to a friend request (accept or reject)
    path(
        "friends-list/", friends_list, name="friends-list"
    ),  # Endpoint to get a list of friends
    path(
        "friend-requests/", friend_requests, name="friend-requests"
    ),  # Endpoint to get a list of pending friend requests
]
