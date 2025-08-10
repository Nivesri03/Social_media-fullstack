#!/usr/bin/env python
import os
import sys
import django

# Setup Django
sys.path.append('.')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'social_media.settings')
django.setup()

from posts.models import Post
from accounts.models import User

def create_sample_reels():
    try:
        # Get the admin user
        admin = User.objects.get(username='admin')
        
        # Create sample YouTube reels with the URLs provided
        youtube_urls = [
            'https://www.youtube.com/shorts/PRM4Ra_ds7o',
            'https://www.youtube.com/shorts/hOvsudKAp_4',
            'https://www.youtube.com/shorts/flFRQT8YWGE',
            'https://youtube.com/shorts/HYo8tXAzSeI?si=etqpdK0oQzEQp_WH'
        ]
        
        for i, url in enumerate(youtube_urls):
            video_id = Post.extract_youtube_id(url)
            if video_id:
                reel = Post.objects.create(
                    author=admin,
                    content=f"Amazing YouTube Short #{i+1}! Check this out! 🔥",
                    post_type='reel',
                    youtube_video_id=video_id
                )
                print(f"Created reel {i+1} with video ID: {video_id}")
        
        print("Sample reels created successfully!")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    create_sample_reels()
