from django.contrib import admin
from .models import Book, Category, Rating, Profile, WishList

admin.site.register(Book)
admin.site.register(Category)
admin.site.register(Rating)
admin.site.register(Profile)
admin.site.register(WishList)

# Register your models here.
