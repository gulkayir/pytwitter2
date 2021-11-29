from django.db import models

from account.models import User


class Tag(models.Model):
    slug = models.SlugField(max_length=50, primary_key=True)
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return str(self.name)


class Tweet(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tweet')
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, related_name='tweet')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text


class Image(models.Model):
    image = models.ImageField(upload_to='images')
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE, related_name='images')


class Comment(models.Model):
    comment = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')

    def __str__(self):
        return str(self.comment)

    class Meta:
        ordering = ('-created',)


class Likes(models.Model):
    likes = models.BooleanField(default=False)
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE, related_name='likes')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')


    def __str__(self):
        return str(self.likes)


class Rating(models.Model):
    rating = models.IntegerField(default=0)
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE, related_name='rating')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rating')

    def __str__(self):
        return str(self.rating)

class Favorite(models.Model):
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE, related_name='favourites')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favourites')
    favorite = models.BooleanField(default=True)


