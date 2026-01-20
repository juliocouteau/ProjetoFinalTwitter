from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    bio = models.TextField(max_length=500, blank=True)
    profile_pic = models.ImageField(upload_to='profile_pics/', default='default.png')
    cover_image = models.ImageField(upload_to='covers/', default='default_cover.png', blank=True)
    following = models.ManyToManyField('self', symmetrical=False, related_name='followers', blank=True)

    
    @property
    def unread_notifications_count(self):
        return self.notifications.filter(is_read=False).count()

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    content = models.TextField(max_length=280, blank=True) # Agora pode ser vazio se tiver foto/video
    image = models.ImageField(upload_to='post_images/', blank=True, null=True)
    video = models.FileField(upload_to='post_videos/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True)
    
    # Sistema de Retweet (Repost)
    repost_of = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='reposts')

    class Meta:
        ordering = ['-created_at']

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(max_length=140)
    created_at = models.DateTimeField(auto_now_add=True)

class Notification(models.Model):
    TYPES = (
        ('L', 'Like'),
        ('C', 'Comentário'),
        ('F', 'Seguidor'),
        ('R', 'Retweet'),
    )
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    from_user = models.ForeignKey(User, on_delete=models.CASCADE)
    notification_type = models.CharField(max_length=1, choices=TYPES)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']