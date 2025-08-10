from django import forms
from .models import Post, Comment
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit, Row, Column


class PostForm(forms.ModelForm):
    youtube_url = forms.URLField(
        required=False,
        widget=forms.URLInput(attrs={
            'placeholder': 'Paste YouTube Shorts URL here...',
            'class': 'form-control'
        }),
        help_text='For reels, paste a YouTube Shorts URL (e.g., https://www.youtube.com/shorts/VIDEO_ID)'
    )

    class Meta:
        model = Post
        fields = ['content', 'caption', 'image', 'video', 'post_type', 'youtube_url']
        widgets = {
            'content': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': "What's on your mind?",
                'class': 'form-control'
            }),
            'caption': forms.Textarea(attrs={
                'rows': 2,
                'placeholder': "Write a caption for your photo/video...",
                'class': 'form-control'
            }),
            'post_type': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('content', css_class='form-control mb-3'),
            Field('caption', css_class='form-control mb-3'),
            Row(
                Column('post_type', css_class='form-group col-md-6 mb-3'),
                Column('youtube_url', css_class='form-group col-md-6 mb-3'),
                css_class='form-row'
            ),
            Row(
                Column('image', css_class='form-group col-md-6 mb-3'),
                Column('video', css_class='form-group col-md-6 mb-3'),
                css_class='form-row'
            ),
            Submit('submit', 'Post', css_class='btn btn-primary btn-block')
        )

    def clean(self):
        cleaned_data = super().clean()
        post_type = cleaned_data.get('post_type')
        image = cleaned_data.get('image')
        video = cleaned_data.get('video')
        content = cleaned_data.get('content')
        youtube_url = cleaned_data.get('youtube_url')

        if post_type == 'image' and not image:
            raise forms.ValidationError("Image is required for image posts.")

        if post_type == 'video' and not video:
            raise forms.ValidationError("Video file is required for video posts.")

        if post_type == 'reel':
            if not youtube_url:
                raise forms.ValidationError("YouTube URL is required for reel posts.")
            # Extract and validate YouTube ID
            video_id = Post.extract_youtube_id(youtube_url)
            if not video_id:
                raise forms.ValidationError("Please provide a valid YouTube URL (e.g., https://www.youtube.com/shorts/VIDEO_ID)")
            cleaned_data['youtube_video_id'] = video_id

        if post_type == 'text' and not content:
            raise forms.ValidationError("Content is required for text posts.")

        return cleaned_data


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.TextInput(attrs={
                'placeholder': 'Write a comment...',
                'class': 'form-control comment-input'
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False
        self.helper.layout = Layout(
            Field('content', css_class='form-control'),
        )
