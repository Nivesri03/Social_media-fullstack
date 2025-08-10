# SocialApp - Mini Social Media Platform

A complete, responsive social media application built with Django and modern web technologies.

## 🚀 Features

### Core Features
- **User Authentication**: Registration, login, logout, password reset
- **User Profiles**: Customizable profiles with bio, profile picture, and stats
- **Posts & Media**: Create text, image, and video posts
- **Reels**: Dedicated video content with vertical scrolling
- **Comments**: Nested commenting system with replies
- **Likes**: Like posts and comments
- **Follow System**: Follow/unfollow users
- **Real-time Interactions**: AJAX-powered likes, comments, and follows

### Pages
- **Homepage**: Personalized feed with posts from followed users
- **Reels Page**: Video-focused content with auto-play
- **Profile Pages**: User profiles with posts grid and stats
- **Explore**: Discover trending content

### Design Features
- **Responsive Design**: Mobile-first approach, works on all devices
- **Modern UI**: Clean, Instagram-inspired interface
- **Smooth Animations**: CSS animations and transitions
- **Dark Mode Support**: Automatic dark mode detection
- **Accessibility**: WCAG compliant with keyboard navigation

## 🛠️ Technology Stack

### Backend
- **Django 4.2**: Web framework
- **SQLite**: Database (easily switchable to PostgreSQL/MySQL)
- **Pillow**: Image processing
- **Python Decouple**: Environment configuration

### Frontend
- **HTML5 & CSS3**: Semantic markup and modern styling
- **Bootstrap 5**: Responsive framework
- **JavaScript (Vanilla)**: Interactive features
- **Font Awesome**: Icons

### Additional Libraries
- **Django Crispy Forms**: Beautiful form rendering
- **WhiteNoise**: Static file serving

## 📦 Installation & Setup

### Prerequisites
- Python 3.8+
- pip (Python package manager)

### Quick Start

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd social-media
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   # Copy .env file and update if needed
   cp .env.example .env
   ```

5. **Run migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

7. **Create sample data (optional)**
   ```bash
   python manage.py create_sample_data
   ```

8. **Run the development server**
   ```bash
   python manage.py runserver
   ```

9. **Access the application**
   - Open your browser and go to `http://127.0.0.1:8000`
   - Admin panel: `http://127.0.0.1:8000/admin`

## 🎮 Demo Accounts

If you ran the sample data command, you can use these demo accounts:

- **Username**: demo1, **Password**: demo123
- **Username**: demo2, **Password**: demo123
- **Username**: demo3, **Password**: demo123

## 📱 Usage

### Creating Posts
1. Click the "Create" button in the navigation
2. Choose post type (text, image, video, reel)
3. Add content and media
4. Click "Post" to share

### Interacting with Posts
- **Like**: Click the heart icon
- **Comment**: Click the comment icon and type your message
- **Share**: Click the share icon to copy the link

### Following Users
1. Visit a user's profile
2. Click the "Follow" button
3. Their posts will appear in your home feed

### Profile Management
1. Click your profile picture in the navigation
2. Select "Edit Profile"
3. Update your information and profile picture

## 🏗️ Project Structure

```
social_media/
├── accounts/           # User authentication and profiles
├── posts/             # Posts, comments, likes
├── core/              # Homepage, reels, explore
├── templates/         # HTML templates
├── static/           # CSS, JavaScript, images
├── media/            # User uploaded files
├── social_media/     # Django project settings
└── manage.py         # Django management script
```

## 🔧 Configuration

### Environment Variables
- `SECRET_KEY`: Django secret key
- `DEBUG`: Debug mode (True/False)

### Database
The app uses SQLite by default. To use PostgreSQL or MySQL:

1. Install the appropriate database adapter
2. Update `DATABASES` in `settings.py`
3. Run migrations

### Media Files
- Profile pictures: `media/profile_pics/`
- Post images: `media/posts/`
- Videos: `media/videos/`

## 🚀 Deployment

### Production Checklist
1. Set `DEBUG=False` in production
2. Configure a production database
3. Set up static file serving
4. Configure email backend for password reset
5. Set up proper media file handling
6. Use environment variables for sensitive data

### Recommended Hosting
- **Heroku**: Easy deployment with PostgreSQL
- **DigitalOcean**: App Platform or Droplets
- **AWS**: EC2 with RDS
- **PythonAnywhere**: Simple Django hosting

## 🧪 Testing

Run the test suite:
```bash
python manage.py test
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

If you encounter any issues:

1. Check the Django documentation
2. Review the error logs
3. Create an issue on GitHub

## 🔮 Future Enhancements

- [ ] Real-time notifications
- [ ] Direct messaging
- [ ] Stories feature
- [ ] Advanced search
- [ ] Content moderation
- [ ] API endpoints
- [ ] Mobile app
- [ ] Video calling
- [ ] Live streaming

## 📸 Screenshots

*Add screenshots of your application here*

---

Built with ❤️ using Django and modern web technologies.
