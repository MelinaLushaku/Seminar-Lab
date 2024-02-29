from django.db import models

class Category(models.Model):
    id = models.AutoField(primary_key=True)
    categoryName = models.CharField(max_length=30)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    objects = models.Manager()

class User(models.Model):
    id = models.AutoField(primary_key=True)
    firstName = models.CharField(max_length=30)
    lastName = models.CharField(max_length=30)
    bio = models.TextField(null = True, blank = True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    objects = models.Manager()

class WishList(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete = models.CASCADE, null = True, blank = True)
    objects = models.Manager()

class Book(models.Model):
    id = models.AutoField(primary_key=True)
    isbn = models.CharField(max_length=13)
    title = models.CharField(max_length=255)
    author = models.CharField(max_length = 255)
    imageUrl = models.CharField(max_length=255)
    yearOfPublication = models.IntegerField()
    publisher = models.CharField(max_length = 255)

    category = models.ForeignKey(Category, on_delete = models.CASCADE, null = True, blank = True)
    wishList = models.ForeignKey(WishList, on_delete = models.CASCADE, null = True, blank = True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    objects = models.Manager()

class Rating(models.Model):
    id = models.AutoField(primary_key=True)
    rating = models.SmallIntegerField()
    isbn = models.CharField(max_length=13)
    user = models.ForeignKey(User, on_delete= models.CASCADE, null = True, blank = True)
    book = models.ForeignKey(Book, on_delete= models.CASCADE, null = True, blank = True)
    objects = models.Manager()
