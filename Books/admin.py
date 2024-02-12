from django.contrib import admin
from .models import Book, Category, Rating, User, WishList

admin.site.register(Book)
admin.site.register(Category)
admin.site.register(Rating)
admin.site.register(User)
admin.site.register(WishList)

# Register your models here.
