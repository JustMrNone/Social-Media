from django.contrib.auth.models import AbstractUser
from django.db import models

# Custom User model inheriting from AbstractUser

class User(AbstractUser):
    # Add a field for profile picture
    picture = models.ImageField(upload_to='profile_pics', default='default.jpg', blank=True)
    
    # Add a field for login attempts
    login_attempts = models.IntegerField(default=0)

    def __str__(self):
        return self.username

# Model to represent the relationship between users for following/followers functionality
class UserFollowing(models.Model):
    user_id = models.ForeignKey("User", on_delete=models.CASCADE, related_name="following")
    following_user_id = models.ForeignKey("User", on_delete=models.CASCADE, related_name="followers")
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together= ('user_id', 'following_user_id')
        ordering = ["-timestamp"]

    def __str__(self):
        return f"{self.user_id} follows {self.following_user_id}"

# Model representing a post

class Post(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="posts")
    body = models.TextField(blank=True)
    comments = models.ForeignKey("Comment", null=True, on_delete=models.CASCADE, related_name="comments")
    total_likes = models.PositiveIntegerField(default=0)
    user_likes = models.ManyToManyField("User", related_name="liked_posts")
    timestamp = models.DateTimeField(auto_now_add=True)
    picture = models.ImageField(upload_to='post_pics', blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.body[:20]}"

# Model representing a comment on a post
class Comment(models.Model):
    id = models.BigAutoField(primary_key=True)  # Explicitly define primary key as BigAutoField
    comment = models.TextField(blank=True)
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="user_comments")
    post = models.ForeignKey("Post", on_delete=models.CASCADE, related_name="post_comments")
    timestamp = models.DateTimeField(auto_now_add=True)

# Model representing a like on a post
class Like(models.Model):
    id = models.BigAutoField(primary_key=True)  # Explicitly define primary key as BigAutoField
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="user_likes")
    post = models.ForeignKey("Post", on_delete=models.CASCADE, related_name="post_likes")
    currently_liked = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)