from django.contrib.auth.models import AbstractUser
from django.db import models


class MyUser(AbstractUser):
    pass


class Category(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class Specialist(models.Model):
    title = models.CharField(max_length=250)
    age = models.IntegerField()
    gender = models.CharField(max_length=100)
    city = models.CharField(max_length=250)
    likes = models.IntegerField()
    front_image = models.CharField(max_length=1000)
    first_image = models.CharField(max_length=1000)
    second_image=models.CharField(max_length=1000)
    third_image=models.CharField(max_length=1000)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="specialists")
    author = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name="specialists", default=1)
    followers = models.ManyToManyField(MyUser)

    class Meta:
        verbose_name = 'Specialist'
        verbose_name_plural = 'Specialist'


class Comment(models.Model):
    title = models.CharField(max_length=100, default='default title')
    text = models.CharField(max_length=1000, default='default text')
    specialist = models.ForeignKey(Specialist, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='comments')

    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'

