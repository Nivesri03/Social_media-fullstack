from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from posts.models import Post, Comment, Like, Save, Share
from accounts.models import Follow
import random

User = get_user_model()


class Command(BaseCommand):
    help = 'Create sample data for the social media app'

    def handle(self, *args, **options):
        self.stdout.write('Creating sample data...')
        
        # Create sample users
        users_data = [
            {
                'username': 'demo1',
                'email': 'demo1@example.com',
                'first_name': 'John',
                'last_name': 'Doe',
                'bio': 'Photography enthusiast and travel lover 📸✈️',
                'password': 'demo123'
            },
            {
                'username': 'demo2',
                'email': 'demo2@example.com',
                'first_name': 'Jane',
                'last_name': 'Smith',
                'bio': 'Tech blogger and coffee addict ☕💻',
                'password': 'demo123'
            },
            {
                'username': 'demo3',
                'email': 'demo3@example.com',
                'first_name': 'Mike',
                'last_name': 'Johnson',
                'bio': 'Fitness trainer and nutrition expert 💪🥗',
                'password': 'demo123'
            },
            {
                'username': 'demo4',
                'email': 'demo4@example.com',
                'first_name': 'Sarah',
                'last_name': 'Wilson',
                'bio': 'Artist and creative soul 🎨✨',
                'password': 'demo123'
            },
            {
                'username': 'demo5',
                'email': 'demo5@example.com',
                'first_name': 'Alex',
                'last_name': 'Brown',
                'bio': 'Music producer and DJ 🎵🎧',
                'password': 'demo123'
            }
        ]
        
        created_users = []
        for user_data in users_data:
            user, created = User.objects.get_or_create(
                username=user_data['username'],
                defaults={
                    'email': user_data['email'],
                    'first_name': user_data['first_name'],
                    'last_name': user_data['last_name'],
                    'bio': user_data['bio'],
                }
            )
            if created:
                user.set_password(user_data['password'])
                user.save()
                self.stdout.write(f'Created user: {user.username}')
            created_users.append(user)
        
        # Create sample posts
        sample_posts = [
            {
                'content': 'Just had an amazing sunset photoshoot! The golden hour never disappoints. 🌅 #photography #sunset #goldenhour',
                'post_type': 'text'
            },
            {
                'content': 'New blog post is live! "10 Tips for Better Code Reviews" - check it out and let me know your thoughts! 💻',
                'post_type': 'text'
            },
            {
                'content': 'Morning workout complete! 💪 Remember, consistency is key. What\'s your favorite exercise?',
                'post_type': 'text'
            },
            {
                'content': 'Working on a new painting today. Sometimes art just flows naturally... 🎨',
                'post_type': 'text'
            },
            {
                'content': 'New track dropping soon! Been working on this beat for weeks. Can\'t wait to share it with you all! 🎵',
                'post_type': 'text'
            },
            {
                'content': 'Coffee and code - the perfect combination for a productive morning! ☕💻 #coding #coffee',
                'post_type': 'text'
            },
            {
                'content': 'Travel tip: Always pack light and bring a good camera. You never know what amazing moments you\'ll capture! 📸✈️',
                'post_type': 'text'
            },
            {
                'content': 'Healthy meal prep Sunday! 🥗 Preparing for a successful week ahead. What\'s your go-to healthy meal?',
                'post_type': 'text'
            },
            {
                'content': 'Art exhibition opening tonight! So excited to showcase my latest collection. See you there! 🎨✨',
                'post_type': 'text'
            },
            {
                'content': 'Late night studio session. The creativity hits different after midnight... 🎧🌙',
                'post_type': 'text'
            },
            {
                'content': 'Check out this amazing dance move! 💃',
                'caption': 'Learning new choreography every day!',
                'post_type': 'reel'
            },
            {
                'content': 'Quick cooking tip for busy weekdays! 👨‍🍳',
                'caption': '30-second pasta hack that will change your life!',
                'post_type': 'video'
            },
            {
                'content': 'Morning motivation to start your day right! 🌅',
                'caption': 'Rise and shine! Every day is a new opportunity.',
                'post_type': 'reel'
            },
            {
                'content': 'Behind the scenes of my latest photoshoot! 📸',
                'caption': 'The magic happens behind the camera too!',
                'post_type': 'video'
            }
        ]
        
        created_posts = []
        for i, post_data in enumerate(sample_posts):
            author = created_users[i % len(created_users)]
            post = Post.objects.create(
                author=author,
                content=post_data['content'],
                caption=post_data.get('caption', ''),
                post_type=post_data['post_type']
            )
            created_posts.append(post)
            self.stdout.write(f'Created post by {author.username}')
        
        # Create sample follows
        for user in created_users:
            # Each user follows 2-3 random other users
            other_users = [u for u in created_users if u != user]
            follows_count = random.randint(2, min(3, len(other_users)))
            to_follow = random.sample(other_users, follows_count)
            
            for follow_user in to_follow:
                Follow.objects.get_or_create(
                    follower=user,
                    following=follow_user
                )
        
        # Create sample likes
        for post in created_posts:
            # Each post gets 1-4 random likes
            likes_count = random.randint(1, 4)
            potential_likers = [u for u in created_users if u != post.author]
            likers = random.sample(potential_likers, min(likes_count, len(potential_likers)))
            
            for liker in likers:
                Like.objects.get_or_create(
                    user=liker,
                    post=post
                )
        
        # Create sample comments
        sample_comments = [
            "Great post! 👍",
            "Love this! 😍",
            "So inspiring! ✨",
            "Thanks for sharing! 🙏",
            "Amazing work! 🔥",
            "This is awesome! 💯",
            "Keep it up! 💪",
            "Beautiful! 😊",
            "Totally agree! 👌",
            "Can't wait to see more! 🎉"
        ]
        
        for post in created_posts:
            # Each post gets 1-3 random comments
            comments_count = random.randint(1, 3)
            potential_commenters = [u for u in created_users if u != post.author]
            commenters = random.sample(potential_commenters, min(comments_count, len(potential_commenters)))

            for commenter in commenters:
                Comment.objects.create(
                    author=commenter,
                    post=post,
                    content=random.choice(sample_comments)
                )

        # Create sample saves
        for post in created_posts:
            # Each post gets 0-2 random saves
            saves_count = random.randint(0, 2)
            potential_savers = [u for u in created_users if u != post.author]
            savers = random.sample(potential_savers, min(saves_count, len(potential_savers)))

            for saver in savers:
                Save.objects.get_or_create(
                    user=saver,
                    post=post
                )

        # Create sample shares
        for post in created_posts:
            # Each post gets 0-1 random shares
            if random.choice([True, False]):
                sharer = random.choice([u for u in created_users if u != post.author])
                Share.objects.create(
                    user=sharer,
                    post=post,
                    share_type=random.choice(['link', 'story', 'direct']),
                    shared_to='Social Media'
                )

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created sample data:\n'
                f'- {len(created_users)} users\n'
                f'- {len(created_posts)} posts\n'
                f'- {Follow.objects.count()} follows\n'
                f'- {Like.objects.count()} likes\n'
                f'- {Comment.objects.count()} comments\n'
                f'- {Save.objects.count()} saves\n'
                f'- {Share.objects.count()} shares'
            )
        )
