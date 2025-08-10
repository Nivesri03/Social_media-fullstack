from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from posts.models import Post
from posts.forms import PostForm
from accounts.models import Follow
from .models import Notification, Message, Story

User = get_user_model()


def home(request):
    if request.user.is_authenticated:
        # Get posts from users the current user follows + their own posts
        following_users = Follow.objects.filter(follower=request.user).values_list('following', flat=True)
        posts = Post.objects.filter(
            Q(author__in=following_users) | Q(author=request.user),
            is_active=True
        ).select_related('author').prefetch_related('likes', 'comments')
    else:
        # Show all posts for anonymous users
        posts = Post.objects.filter(is_active=True).select_related('author').prefetch_related('likes', 'comments')

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
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Post form for authenticated users
    post_form = PostForm() if request.user.is_authenticated else None

    context = {
        'posts': page_obj,
        'post_form': post_form,
    }
    return render(request, 'core/home.html', context)


def reels(request):
    # Filter for reel type posts (YouTube videos)
    reels = Post.objects.filter(
        post_type='reel',
        is_active=True
    ).select_related('author').prefetch_related('likes', 'comments').order_by('-created_at')

    # Add like and save status for each reel
    if request.user.is_authenticated:
        for reel in reels:
            reel.user_has_liked = reel.is_liked_by(request.user)
            reel.user_has_saved = reel.is_saved_by(request.user)
    else:
        for reel in reels:
            reel.user_has_liked = False
            reel.user_has_saved = False

    # No pagination for YouTube Shorts-style experience
    context = {
        'reels': reels,
    }
    return render(request, 'core/reels.html', context)


def explore(request):
    # Show trending/popular posts (ordered by likes and comments)
    posts = Post.objects.filter(is_active=True).select_related('author').prefetch_related('likes', 'comments')

    # Add like and save status for each post
    if request.user.is_authenticated:
        for post in posts:
            post.user_has_liked = post.is_liked_by(request.user)
            post.user_has_saved = post.is_saved_by(request.user)
    else:
        for post in posts:
            post.user_has_liked = False
            post.user_has_saved = False

    # Simple trending algorithm - posts with most engagement
    posts = sorted(posts, key=lambda x: x.likes_count + x.comments_count, reverse=True)

    # Pagination
    paginator = Paginator(posts, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'posts': page_obj,
    }
    return render(request, 'core/explore.html', context)


@login_required
def notifications(request):
    notifications = Notification.objects.filter(recipient=request.user)

    # Mark all as read when viewing
    notifications.update(is_read=True)

    # Pagination
    paginator = Paginator(notifications, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'notifications': page_obj,
    }
    return render(request, 'core/notifications.html', context)


@login_required
def notification_count(request):
    count = Notification.objects.filter(recipient=request.user, is_read=False).count()
    return JsonResponse({'count': count})


@login_required
def messages(request):
    # Get all users with same credentials for demo chat
    demo_users = User.objects.filter(email='xyz@gmail.com').exclude(id=request.user.id)

    # Get recent messages
    messages = Message.objects.filter(
        Q(sender=request.user) | Q(recipient=request.user)
    ).select_related('sender', 'recipient')[:50]

    context = {
        'demo_users': demo_users,
        'messages': messages,
    }
    return render(request, 'core/messages.html', context)


@login_required
def send_message(request):
    if request.method == 'POST':
        recipient_id = request.POST.get('recipient_id')
        content = request.POST.get('content')

        if recipient_id and content:
            recipient = User.objects.get(id=recipient_id)
            message = Message.objects.create(
                sender=request.user,
                recipient=recipient,
                content=content
            )

            return JsonResponse({
                'status': 'success',
                'message': {
                    'id': message.id,
                    'content': message.content,
                    'sender': message.sender.username,
                    'created_at': message.created_at.strftime('%H:%M')
                }
            })

    return JsonResponse({'status': 'error'})


@login_required
def message_count(request):
    count = Message.objects.filter(recipient=request.user, is_read=False).count()
    return JsonResponse({'count': count})
