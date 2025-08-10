// Main JavaScript for Social Media App

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // CSRF Token setup for AJAX requests
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    const csrftoken = getCookie('csrftoken');

    // Like/Unlike Post functionality
    document.addEventListener('click', function(e) {
        if (e.target.classList.contains('like-btn') || e.target.closest('.like-btn')) {
            e.preventDefault();
            const btn = e.target.classList.contains('like-btn') ? e.target : e.target.closest('.like-btn');
            const postId = btn.dataset.postId;
            
            fetch('/posts/like/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'X-CSRFToken': csrftoken,
                },
                body: `post_id=${postId}`
            })
            .then(response => response.json())
            .then(data => {
                const icon = btn.querySelector('i');
                const countSpan = btn.querySelector('.like-count');
                
                if (data.status === 'liked') {
                    icon.classList.remove('far');
                    icon.classList.add('fas');
                    btn.classList.add('liked');
                    btn.classList.add('pulse');
                } else {
                    icon.classList.remove('fas');
                    icon.classList.add('far');
                    btn.classList.remove('liked');
                }
                
                countSpan.textContent = data.likes_count;
                
                // Remove pulse animation after it completes
                setTimeout(() => btn.classList.remove('pulse'), 300);
            })
            .catch(error => console.error('Error:', error));
        }
    });

    // Follow/Unfollow functionality
    document.addEventListener('click', function(e) {
        if (e.target.classList.contains('follow-btn')) {
            e.preventDefault();
            const btn = e.target;
            const username = btn.dataset.username;
            const action = btn.textContent.trim() === 'Follow' ? 'follow' : 'unfollow';
            
            fetch(`/accounts/${action}/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'X-CSRFToken': csrftoken,
                },
                body: `username=${username}`
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'followed') {
                    btn.textContent = 'Unfollow';
                    btn.classList.remove('btn-primary');
                    btn.classList.add('btn-outline-primary');
                } else if (data.status === 'unfollowed') {
                    btn.textContent = 'Follow';
                    btn.classList.remove('btn-outline-primary');
                    btn.classList.add('btn-primary');
                }
                
                // Update followers count if element exists
                const followersCount = document.querySelector('.followers-count');
                if (followersCount) {
                    followersCount.textContent = data.followers_count;
                }
            })
            .catch(error => console.error('Error:', error));
        }
    });

    // Add Comment functionality
    document.addEventListener('submit', function(e) {
        if (e.target.classList.contains('comment-form')) {
            e.preventDefault();
            const form = e.target;
            const postId = form.dataset.postId;
            const content = form.querySelector('input[name="content"]').value.trim();
            
            if (!content) return;
            
            fetch('/posts/comment/add/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'X-CSRFToken': csrftoken,
                },
                body: `post_id=${postId}&content=${encodeURIComponent(content)}`
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    // Add new comment to the comments section
                    const commentsSection = form.closest('.post-card').querySelector('.comments-section');
                    const newComment = createCommentElement(data.comment);
                    commentsSection.appendChild(newComment);
                    
                    // Clear the form
                    form.querySelector('input[name="content"]').value = '';
                    
                    // Update comments count
                    const commentsCount = form.closest('.post-card').querySelector('.comments-count');
                    if (commentsCount) {
                        commentsCount.textContent = data.comments_count;
                    }
                    
                    // Add fade-in animation
                    newComment.classList.add('fade-in');
                }
            })
            .catch(error => console.error('Error:', error));
        }
    });

    // Create comment element
    function createCommentElement(comment) {
        const div = document.createElement('div');
        div.className = 'comment-item';
        div.innerHTML = `
            <div class="d-flex">
                <img src="${comment.author_profile_pic || '/static/images/default-avatar.png'}" 
                     alt="${comment.author}" class="rounded-circle me-2" 
                     style="width: 32px; height: 32px; object-fit: cover;">
                <div class="flex-grow-1">
                    <span class="comment-author">${comment.author}</span>
                    <span class="comment-content">${comment.content}</span>
                    <div class="comment-meta">
                        <small class="comment-time text-muted">${comment.created_at}</small>
                    </div>
                </div>
            </div>
        `;
        return div;
    }

    // Infinite scroll for posts (optional enhancement)
    let loading = false;
    window.addEventListener('scroll', function() {
        if (loading) return;
        
        if (window.innerHeight + window.scrollY >= document.body.offsetHeight - 1000) {
            const nextPageUrl = document.querySelector('.pagination .page-item:last-child a')?.href;
            if (nextPageUrl && !nextPageUrl.includes('#')) {
                loading = true;
                loadMorePosts(nextPageUrl);
            }
        }
    });

    function loadMorePosts(url) {
        fetch(url)
        .then(response => response.text())
        .then(html => {
            const parser = new DOMParser();
            const doc = parser.parseFromString(html, 'text/html');
            const newPosts = doc.querySelectorAll('.post-card');
            const postsContainer = document.querySelector('.posts-container');
            
            newPosts.forEach(post => {
                post.classList.add('fade-in');
                postsContainer.appendChild(post);
            });
            
            // Update pagination
            const newPagination = doc.querySelector('.pagination');
            const currentPagination = document.querySelector('.pagination');
            if (newPagination && currentPagination) {
                currentPagination.innerHTML = newPagination.innerHTML;
            }
            
            loading = false;
        })
        .catch(error => {
            console.error('Error loading more posts:', error);
            loading = false;
        });
    }

    // Image preview for post creation
    const imageInput = document.querySelector('input[type="file"][accept*="image"]');
    if (imageInput) {
        imageInput.addEventListener('change', function(e) {
            const file = e.target.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    let preview = document.querySelector('.image-preview');
                    if (!preview) {
                        preview = document.createElement('div');
                        preview.className = 'image-preview mt-3';
                        imageInput.parentNode.appendChild(preview);
                    }
                    preview.innerHTML = `
                        <img src="${e.target.result}" alt="Preview" 
                             class="img-fluid rounded" style="max-height: 300px;">
                        <button type="button" class="btn btn-sm btn-danger mt-2" onclick="this.parentNode.remove(); document.querySelector('input[type=file]').value='';">
                            Remove
                        </button>
                    `;
                };
                reader.readAsDataURL(file);
            }
        });
    }

    // Auto-resize textarea
    const textareas = document.querySelectorAll('textarea');
    textareas.forEach(textarea => {
        textarea.addEventListener('input', function() {
            this.style.height = 'auto';
            this.style.height = this.scrollHeight + 'px';
        });
    });
});
