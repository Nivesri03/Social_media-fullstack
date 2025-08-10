from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Post, Like, Comment, CommentLike, Save, Share
from .forms import PostForm, CommentForm
from core.models import Notification


@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user

            # Handle YouTube URL for reels
            if form.cleaned_data.get('youtube_video_id'):
                post.youtube_video_id = form.cleaned_data['youtube_video_id']

            post.save()
            messages.success(request, 'Post created successfully!')

            # Redirect to reels page if it's a reel
            if post.post_type == 'reel':
                messages.success(request, 'Reel created successfully! 🎬')
                return redirect('core:reels')
            return redirect('core:home')
    else:
        # Check if type parameter is provided (e.g., ?type=reel)
        initial_data = {}
        post_type = request.GET.get('type')
        if post_type in ['text', 'image', 'video', 'reel']:
            initial_data['post_type'] = post_type

        form = PostForm(initial=initial_data)

    return render(request, 'posts/create_post.html', {'form': form})


def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id, is_active=True)
    comments = Comment.objects.filter(post=post, is_active=True, parent=None)
    comment_form = CommentForm()

    # Add like and save status for the post
    if request.user.is_authenticated:
        post.user_has_liked = post.is_liked_by(request.user)
        post.user_has_saved = post.is_saved_by(request.user)
    else:
        post.user_has_liked = False
        post.user_has_saved = False

    context = {
        'post': post,
        'comments': comments,
        'comment_form': comment_form,
    }
    return render(request, 'posts/post_detail.html', context)


@login_required
@require_POST
def like_post(request):
    post_id = request.POST.get('post_id')
    post = get_object_or_404(Post, id=post_id)
    
    like, created = Like.objects.get_or_create(user=request.user, post=post)

    if created:
        # Create notification for post author (if not liking own post)
        if post.author != request.user:
            Notification.objects.create(
                recipient=post.author,
                sender=request.user,
                notification_type='like',
                message=f'{request.user.username} liked your post',
                post=post
            )

        return JsonResponse({
            'status': 'liked',
            'likes_count': post.likes_count
        })
    else:
        like.delete()
        # Remove notification if it exists
        Notification.objects.filter(
            recipient=post.author,
            sender=request.user,
            notification_type='like',
            post=post
        ).delete()

        return JsonResponse({
            'status': 'unliked',
            'likes_count': post.likes_count
        })


@login_required
@require_POST
def add_comment(request):
    post_id = request.POST.get('post_id')
    content = request.POST.get('content')
    parent_id = request.POST.get('parent_id')
    
    post = get_object_or_404(Post, id=post_id)
    
    if not content.strip():
        return JsonResponse({'error': 'Comment cannot be empty'}, status=400)
    
    comment = Comment.objects.create(
        author=request.user,
        post=post,
        content=content,
        parent_id=parent_id if parent_id else None
    )

    # Create notification for post author (if not commenting on own post)
    if post.author != request.user:
        Notification.objects.create(
            recipient=post.author,
            sender=request.user,
            notification_type='comment',
            message=f'{request.user.username} commented on your post',
            post=post
        )

    return JsonResponse({
        'status': 'success',
        'comment': {
            'id': comment.id,
            'content': comment.content,
            'author': comment.author.username,
            'author_profile_pic': comment.author.profile_picture.url if comment.author.profile_picture else None,
            'created_at': comment.created_at.strftime('%Y-%m-%d %H:%M'),
            'replies_count': comment.replies_count
        },
        'comments_count': post.comments_count
    })


@login_required
@require_POST
def like_comment(request):
    comment_id = request.POST.get('comment_id')
    comment = get_object_or_404(Comment, id=comment_id)
    
    like, created = CommentLike.objects.get_or_create(
        user=request.user, 
        comment=comment
    )
    
    if created:
        return JsonResponse({
            'status': 'liked',
            'likes_count': comment.likes.count()
        })
    else:
        like.delete()
        return JsonResponse({
            'status': 'unliked',
            'likes_count': comment.likes.count()
        })


@login_required
@require_POST
def save_post(request):
    post_id = request.POST.get('post_id')
    post = get_object_or_404(Post, id=post_id)

    save, created = Save.objects.get_or_create(
        user=request.user,
        post=post
    )

    if created:
        return JsonResponse({
            'status': 'saved',
            'saves_count': post.saves_count
        })
    else:
        save.delete()
        return JsonResponse({
            'status': 'unsaved',
            'saves_count': post.saves_count
        })


@login_required
@require_POST
def share_post(request):
    post_id = request.POST.get('post_id')
    share_type = request.POST.get('share_type', 'link')
    shared_to = request.POST.get('shared_to', '')

    post = get_object_or_404(Post, id=post_id)

    share = Share.objects.create(
        user=request.user,
        post=post,
        share_type=share_type,
        shared_to=shared_to
    )

    return JsonResponse({
        'status': 'shared',
        'shares_count': post.shares_count,
        'share_id': share.id
    })


@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, author=request.user)
    
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Post updated successfully!')
            return redirect('posts:detail', post_id=post.id)
    else:
        form = PostForm(instance=post)
    
    return render(request, 'posts/edit_post.html', {'form': form, 'post': post})


@login_required
@require_POST
def delete_post(request):
    post_id = request.POST.get('post_id')
    post = get_object_or_404(Post, id=post_id, author=request.user)
    post.is_active = False
    post.save()
    
    return JsonResponse({'status': 'deleted'})


def search_posts(request):
    query = request.GET.get('q', '')
    posts = Post.objects.filter(is_active=True)

    if query:
        posts = posts.filter(
            Q(content__icontains=query) |
            Q(author__username__icontains=query) |
            Q(author__first_name__icontains=query) |
            Q(author__last_name__icontains=query)
        )

    # Add like and save status for each post
    if request.user.is_authenticated:
        for post in posts:
            post.user_has_liked = post.is_liked_by(request.user)
            post.user_has_saved = post.is_saved_by(request.user)
    else:
        for post in posts:
            post.user_has_liked = False
            post.user_has_saved = False

    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'posts': page_obj,
        'query': query,
    }
    return render(request, 'posts/search_results.html', context)
