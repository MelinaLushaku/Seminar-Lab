"""
URL configuration for BookRecommender project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from Books import views

urlpatterns = [
    path('', views.index),
    path('admin/', admin.site.urls),
    path('books/<int:id>', views.book_details, name='view-book'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('login-user', views.login_user, name="login"),
    path('register-user', views.register_user),
    path('logout-user', views.logout_user, name="logout"),
    path('profile', views.user_profile, name="profile"),
    path('wish-list', views.wish_list),
    path('add-Category' , views.manage_categories),
    path('save-book/<int:id>', views.save_book_to_wishlist, name="save-book"),
    path('remove-book/<int:id>', views.remove_book_to_wishlist, name="remove-book"),
    path('manage_categories' , views.manage_categories),
    path('rate/<int:book_id>' ,views.rate_book,  name="rate-book" ),
    path('add-book/', views.add_book, name='add_book')
]
 