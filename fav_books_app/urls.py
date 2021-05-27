from django.urls import path
from . import views
urlpatterns = [
#login and registration
    path('', views.index),
    path('register/', views.register),
    path('login/', views.login),
    path('logout/', views.logout),
#books
    path('books/', views.books),
    path('books/<int:book_id>', views.edit_book),
    path('books/<int:book_id>/update', views.book_update),
    path('books/<int:book_id>/delete', views.delete_book), #this is a redirect
    path('create/<int:user_id>', views.create_book), #this is a redirect
    path('favorite/<int:book_id>', views.favorite),
]