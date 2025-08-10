from django import template
import os

register = template.Library()


@register.filter
def safe_profile_picture_url(user):
    """
    Safely get profile picture URL, return None if file doesn't exist
    """
    if not user or not user.profile_picture:
        return None
    
    try:
        # Try to access the URL, this will raise an exception if file doesn't exist
        url = user.profile_picture.url
        # Additional check to see if file exists
        if user.profile_picture.file:
            return url
    except (ValueError, FileNotFoundError, OSError):
        return None
    
    return None


@register.filter
def has_valid_profile_picture(user):
    """
    Check if user has a valid profile picture file
    """
    if not user or not user.profile_picture:
        return False
    
    try:
        # Try to access the file
        if user.profile_picture.file:
            return True
    except (ValueError, FileNotFoundError, OSError):
        return False
    
    return False
