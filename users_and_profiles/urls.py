from django.urls import path, include

from .views import *


urlpatterns = [
    path('', friends_list, name='friends-list'),
    path('inbox/', inbox, name='inbox'),
    path('edit_profile/', edit_profile, name='edit-profile'),
    path('add_friend/', add_friend, name='add-friend'),
    path('register/', register, name='register'),
    path('accept-friend-request/<int:request_id>/', accept_friend_request, name='accept-friend-request'),
    path('reject-friend-request/<int:request_id>/', reject_friend_request, name='reject-friend-request'),
]
