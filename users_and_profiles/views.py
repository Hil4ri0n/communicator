from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from chat.models import ChatRoom
from .forms import *
from .models import Profile, FriendRequest


@login_required
def edit_profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('friends-list')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'users_and_profiles/profiles/edit_profile.html', context)


@login_required
def friends_list(request):
    profile = Profile.objects.get(user=request.user)
    friends = profile.friends.all()
    context = {'friends': friends, 'profile': profile}
    return render(request, 'users_and_profiles/profiles/friends_list.html', context)


@login_required
def add_friend(request):
    if request.method == "POST":
        nickname = request.POST.get("nickname")
        try:
            to_user_profile = Profile.objects.get(nickname=nickname)
            from_user_profile = request.user.profile

            if to_user_profile == from_user_profile:
                messages.error(request, "You cannot send a friend request to yourself.")
                return redirect('add-friend')

            profile = request.user.profile
            friends = profile.friends.all()

            if to_user_profile in friends:
                messages.error(request, "This user is your friend already!")
                return redirect('add-friend')

            if FriendRequest.objects.filter(from_user=from_user_profile, to_user=to_user_profile).exists():
                messages.error(request, "Friend request already sent.")
            else:
                FriendRequest.objects.create(from_user=from_user_profile, to_user=to_user_profile)
                messages.success(request, "Friend request sent successfully.")

        except Profile.DoesNotExist:
            messages.error(request, "User with that nickname does not exist.")

    return render(request, 'users_and_profiles/profiles/add_friend.html')


@login_required
def inbox(request):
    profile = request.user.profile
    friend_requests = FriendRequest.objects.filter(to_user=profile)
    context = {'friend_requests': friend_requests}
    return render(request, 'users_and_profiles/profiles/inbox.html', context)


@require_POST
def accept_friend_request(request, request_id):
    friend_request = get_object_or_404(FriendRequest, id=request_id)
    if friend_request.to_user.user == request.user:
        # Adding each other as friends
        to_user_profile = friend_request.to_user
        from_user_profile = friend_request.from_user
        to_user_profile.friends.add(from_user_profile)
        from_user_profile.friends.add(to_user_profile)

        # Create a new ChatRoom and add both profiles as participants
        chat_room = ChatRoom.objects.create()  # Creating a new ChatRoom instance
        chat_room.participants.add(to_user_profile, from_user_profile)  # Adding both users as participants

        # Delete the FriendRequest as it's accepted
        friend_request.delete()

    return redirect('inbox')


@require_POST
def reject_friend_request(request, request_id):
    friend_request = get_object_or_404(FriendRequest, id=request_id)
    if friend_request.to_user.user == request.user:
        friend_request.delete()
    return redirect('inbox')


def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            profile = Profile.objects.create(user=user, nickname=form.cleaned_data['nickname'])
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users_and_profiles/auth/register.html', {'form': form})


