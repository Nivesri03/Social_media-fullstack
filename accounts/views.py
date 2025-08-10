from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
from .forms import CustomUserCreationForm, UserProfileForm
from .models import Follow
from posts.models import Post

User = get_user_model()


def custom_login(request):
    if request.method == 'POST':
        email = request.POST.get('username')  # Django login view uses 'username' field
        password = request.POST.get('password')

        # Handle demo credentials
        if email == 'xyz@gmail.com' and password == 'abcdefghijk':
            try:
                user = User.objects.get(email='xyz@gmail.com')
                login(request, user)
                messages.success(request, 'Welcome to Xeox!')
                return redirect('core:home')
            except User.DoesNotExist:
                messages.error(request, 'Demo user not found. Please contact support.')
        else:
            # Try to authenticate with email as username
            try:
                user = User.objects.get(email=email)
                user = authenticate(request, username=user.username, password=password)
                if user:
                    login(request, user)
                    messages.success(request, 'Welcome back!')
                    return redirect('core:home')
                else:
                    messages.error(request, 'Invalid credentials.')
            except User.DoesNotExist:
                messages.error(request, 'User not found.')

    # Check for demo parameter
    if request.GET.get('demo') == 'true':
        try:
            user = User.objects.get(email='xyz@gmail.com')
            login(request, user)
            messages.success(request, 'Welcome to Xeox Demo!')
            return redirect('core:home')
        except User.DoesNotExist:
            messages.error(request, 'Demo user not found.')

    return render(request, 'accounts/login.html')


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('core:home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})


@login_required
def profile(request, username):
    user = get_object_or_404(User, username=username)
    posts = Post.objects.filter(author=user, is_active=True)

    # Add like and save status for each post
    if request.user.is_authenticated:
        for post in posts:
            post.user_has_liked = post.is_liked_by(request.user)
            post.user_has_saved = post.is_saved_by(request.user)
    else:
        for post in posts:
            post.user_has_liked = False
            post.user_has_saved = False

    # Pagination
    paginator = Paginator(posts, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Check if current user follows this user
    is_following = False
    if request.user.is_authenticated and request.user != user:
        is_following = Follow.objects.filter(
            follower=request.user,
            following=user
        ).exists()

    # Get activity data for own profile
    liked_posts = []
    saved_posts = []
    user_comments = []

    if request.user == user:  # Only show activity for own profile
        from posts.models import Like, Save, Comment

        # Get liked posts
        liked_posts = Post.objects.filter(
            likes__user=user,
            is_active=True
        ).select_related('author').prefetch_related('likes', 'comments')[:20]

        # Get saved posts
        saved_posts = Post.objects.filter(
            saves__user=user,
            is_active=True
        ).select_related('author').prefetch_related('likes', 'comments')[:20]

        # Get user's comments
        user_comments = Comment.objects.filter(
            author=user,
            is_active=True
        ).select_related('post', 'post__author').order_by('-created_at')[:20]

    context = {
        'profile_user': user,
        'posts': page_obj,
        'is_following': is_following,
        'is_own_profile': request.user == user,
        'liked_posts': liked_posts,
        'saved_posts': saved_posts,
        'user_comments': user_comments,
    }
    return render(request, 'accounts/profile.html', context)


@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('accounts:profile', username=request.user.username)
    else:
        form = UserProfileForm(instance=request.user)
    return render(request, 'accounts/edit_profile.html', {'form': form})


@login_required
@require_POST
def follow_user(request):
    username = request.POST.get('username')
    user_to_follow = get_object_or_404(User, username=username)
    
    if request.user == user_to_follow:
        return JsonResponse({'error': 'You cannot follow yourself'}, status=400)
    
    follow, created = Follow.objects.get_or_create(
        follower=request.user,
        following=user_to_follow
    )
    
    if created:
        return JsonResponse({
            'status': 'followed',
            'followers_count': user_to_follow.followers_count
        })
    else:
        return JsonResponse({'error': 'Already following'}, status=400)


@login_required
@require_POST
def unfollow_user(request):
    username = request.POST.get('username')
    user_to_unfollow = get_object_or_404(User, username=username)
    
    try:
        follow = Follow.objects.get(
            follower=request.user,
            following=user_to_unfollow
        )
        follow.delete()
        return JsonResponse({
            'status': 'unfollowed',
            'followers_count': user_to_unfollow.followers_count
        })
    except Follow.DoesNotExist:
        return JsonResponse({'error': 'Not following'}, status=400)


@login_required
def followers_list(request, username):
    user = get_object_or_404(User, username=username)
    followers = Follow.objects.filter(following=user).select_related('follower')
    
    paginator = Paginator(followers, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'profile_user': user,
        'followers': page_obj,
        'list_type': 'followers'
    }
    return render(request, 'accounts/follow_list.html', context)


@login_required
def following_list(request, username):
    user = get_object_or_404(User, username=username)
    following = Follow.objects.filter(follower=user).select_related('following')
    
    paginator = Paginator(following, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'profile_user': user,
        'following': page_obj,
        'list_type': 'following'
    }
    return render(request, 'accounts/follow_list.html', context)
