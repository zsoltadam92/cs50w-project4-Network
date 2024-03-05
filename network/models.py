from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def like_count(self):
        # A property that counts and returns the number of likes a post has received.
        # `like_set` is a reverse lookup to access all Like instances related to this Post instance.
        return self.like_set.count()
        
    def is_liked_by_user(self, user):
        # Check if a post is liked by a given user.
        return self.like_set.filter(user=user).exists()

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    class Meta:
        # Ensures that a user can only like a specific post once.
        unique_together = ('user', 'post')
