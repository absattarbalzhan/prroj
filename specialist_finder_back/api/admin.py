from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin

from .models import Category, Specialist, MyUser, Comment

# admin.site.register(Category)
# admin.site.register(Specialist)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(Specialist)
class SpecialistAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'category')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'specialist')


@admin.register(MyUser)
class MyUserAdmin(UserAdmin):
    list_display = ('username', 'first_name', 'last_name', 'is_superuser')
