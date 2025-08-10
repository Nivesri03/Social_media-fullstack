from django.db import models
from django.contrib.auth import get_user_model
from PIL import Image
import os
import re

User = get_user_model()


class Post(models.Model):
    POST_TYPES = [
        ('image', 'Image'),
        ('video', 'Video'),
        ('text', 'Text'),
        ('reel', 'Reel'),
    ]

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    content = models.TextField(max_length=2000, blank=True)
    caption = models.TextField(max_length=500, blank=True, help_text='Caption for photos/videos')
    image = models.ImageField(upload_to='posts/', blank=True, null=True)
    video = models.FileField(upload_to='videos/', blank=True, null=True)
    youtube_video_id = models.CharField(max_length=20, blank=True, null=True, help_text='YouTube video ID for reels')
    post_type = models.CharField(max_length=10, choices=POST_TYPES, default='text')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.author.username} - {self.post_type} - {self.created_at.strftime('%Y-%m-%d')}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
        if self.image:
            img = Image.open(self.image.path)
            if img.height > 800 or img.width > 800:
                output_size = (800, 800)
                img.thumbnail(output_size)
                img.save(self.image.path)

    @property
    def likes_count(self):
        return self.likes.count()

    @property
    def comments_count(self):
        return self.comments.count()

    def is_liked_by(self, user):
        if user.is_authenticated:
            return self.likes.filter(user=user).exists()
        return False

    def is_saved_by(self, user):
        if user.is_authenticated:
            return self.saves.filter(user=user).exists()
        return False

    @property
    def saves_count(self):
        return self.saves.count()

    @property
    def shares_count(self):
        return self.shares.count()

    @staticmethod
    def extract_youtube_id(url):
        """Extract YouTube video ID from various YouTube URL formats"""
        if not url:
            return None

        # YouTube URL patterns (including shorts with query parameters)
        patterns = [
            r'youtube\.com/watch\?v=([a-zA-Z0-9_-]+)',
            r'youtu\.be/([a-zA-Z0-9_-]+)',
            r'youtube\.com/embed/([a-zA-Z0-9_-]+)',
            r'youtube\.com/shorts/([a-zA-Z0-9_-]+)',
            r'youtube\.com/shorts/([a-zA-Z0-9_-]+)\?',  # With query parameters
        ]

        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)

        return None

    @property
    def youtube_embed_url(self):
        """Get YouTube embed URL for the video (for fallback use)"""
        if self.youtube_video_id:
            return f"https://www.youtube.com/embed/{self.youtube_video_id}?autoplay=1&mute=1&loop=1&playlist={self.youtube_video_id}&controls=0&showinfo=0&rel=0&modestbranding=1&playsinline=1"
        return None

    @property
    def youtube_thumbnail_url(self):
        """Get YouTube thumbnail URL"""
        if self.youtube_video_id:
            return f"https://img.youtube.com/vi/{self.youtube_video_id}/maxresdefault.jpg"
        return None


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} likes {self.post.id}"


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField(max_length=500)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"{self.author.username} - {self.content[:50]}"

    @property
    def replies_count(self):
        return self.replies.filter(is_active=True).count()


class CommentLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comment_likes')
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'comment')

    def __str__(self):
        return f"{self.user.username} likes comment {self.comment.id}"


class Save(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='saves')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='saves')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} saved {self.post.id}"


class Share(models.Model):
    SHARE_TYPES = [
        ('link', 'Link Share'),
        ('story', 'Story Share'),
        ('direct', 'Direct Message'),
        ('external', 'External Platform'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='shares')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='shares')
    share_type = models.CharField(max_length=10, choices=SHARE_TYPES, default='link')
    shared_to = models.CharField(max_length=100, blank=True)  # Platform or user shared to
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} shared {self.post.id} via {self.share_type}"
