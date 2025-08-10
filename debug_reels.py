#!/usr/bin/env python
import os
import sys
import django

# Setup Django
sys.path.append('.')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'social_media.settings')
django.setup()

from posts.models import Post

def debug_reels():
    print("=== REELS DEBUG INFO ===")
    
    # Get all reels
    reels = Post.objects.filter(post_type='reel', is_active=True).order_by('-created_at')
    print(f"Total reels found: {reels.count()}")
    
    for i, reel in enumerate(reels, 1):
        print(f"\n--- Reel {i} ---")
        print(f"ID: {reel.id}")
        print(f"Author: {reel.author.username}")
        print(f"Content: {reel.content}")
        print(f"YouTube Video ID: {reel.youtube_video_id}")
        print(f"Created: {reel.created_at}")
        print(f"Embed URL: {reel.youtube_embed_url}")
        print(f"Thumbnail URL: {reel.youtube_thumbnail_url}")
    
    # Test URL extraction
    print("\n=== URL EXTRACTION TESTS ===")
    test_urls = [
        'https://www.youtube.com/shorts/PRM4Ra_ds7o',
        'https://www.youtube.com/shorts/hOvsudKAp_4', 
        'https://www.youtube.com/shorts/flFRQT8YWGE',
        'https://youtube.com/shorts/HYo8tXAzSeI?si=etqpdK0oQzEQp_WH'
    ]
    
    for url in test_urls:
        video_id = Post.extract_youtube_id(url)
        print(f"URL: {url}")
        print(f"Extracted ID: {video_id}")
        print()

if __name__ == '__main__':
    debug_reels()
