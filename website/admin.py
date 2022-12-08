from django.contrib import admin

from .models import Profile, Course, Book

# Register your models here.
admin.site.register(Profile)
admin.site.register(Course)
admin.site.register(Book)