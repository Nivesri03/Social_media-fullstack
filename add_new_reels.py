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

def add_reels():
    try:
        # Get admin user
        admin = User.objects.get(username='admin')
        
        # Delete existing reels
        Post.objects.filter(post_type='reel').delete()
        print('Deleted existing reels')
        
        # YouTube URLs and content
        reels_data = [
            {
                'url': 'https://www.youtube.com/shorts/YRj7xwxbzSg',
                'content': 'Amazing new viral video! 🔥 #viral #trending #amazing'
            },
            {
                'url': 'https://www.youtube.com/shorts/hOvsudKAp_4',
                'content': 'Incredible talent showcase! 🎭 #talent #skills #awesome'
            },
            {
                'url': 'https://www.youtube.com/shorts/PRM4Ra_ds7o',
                'content': 'Mind-blowing dance moves! 💃 #dance #moves #epic'
            },
            {
                'url': 'https://www.youtube.com/shorts/HYo8tXAzSeI',
                'content': 'Epic moment captured! 📸 #moment #capture #wow'
            }
        ]
        
        for i, reel_data in enumerate(reels_data, 1):
            video_id = Post.extract_youtube_id(reel_data['url'])
            if video_id:
                reel = Post.objects.create(
                    author=admin,
                    content=reel_data['content'],
                    post_type='reel',
                    youtube_video_id=video_id
                )
                print(f'✓ Reel {i}: {video_id} - {reel_data["content"][:30]}...')
            else:
                print(f'✗ Failed to extract video ID from: {reel_data["url"]}')
        
        total = Post.objects.filter(post_type='reel').count()
        print(f'\nSuccess! Created {total} reels')
        
    except Exception as e:
        print(f'Error: {e}')

if __name__ == '__main__':
    add_reels()
