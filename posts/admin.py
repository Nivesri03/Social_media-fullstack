from django.contrib import admin
from .models import Post, Like, Comment, CommentLike, Save, Share


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['author', 'post_type', 'content_preview', 'likes_count', 'comments_count', 'saves_count', 'shares_count', 'created_at', 'is_active']
    list_filter = ['post_type', 'is_active', 'created_at']
    search_fields = ['author__username', 'content']
    ordering = ['-created_at']
    list_per_page = 20

    def content_preview(self, obj):
        return obj.content[:50] + "..." if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'Content Preview'


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ['user', 'post', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'post__content']
    ordering = ['-created_at']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['author', 'post', 'content_preview', 'parent', 'created_at', 'is_active']
    list_filter = ['is_active', 'created_at']
    search_fields = ['author__username', 'content', 'post__content']
    ordering = ['-created_at']

    def content_preview(self, obj):
        return obj.content[:50] + "..." if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'Content Preview'


@admin.register(CommentLike)
class CommentLikeAdmin(admin.ModelAdmin):
    list_display = ['user', 'comment', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'comment__content']
    ordering = ['-created_at']


@admin.register(Save)
class SaveAdmin(admin.ModelAdmin):
    list_display = ['user', 'post', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'post__content']
    ordering = ['-created_at']


@admin.register(Share)
class ShareAdmin(admin.ModelAdmin):
    list_display = ['user', 'post', 'share_type', 'shared_to', 'created_at']
    list_filter = ['share_type', 'created_at']
    search_fields = ['user__username', 'post__content', 'shared_to']
    ordering = ['-created_at']
