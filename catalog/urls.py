from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('allbooks/', views.AllBooksListView.as_view(), name='all-books'),
    path('book/<slug:slug>/', views.BookDetailView.as_view(), name='book'),
    path('allauthors/', views.AllAuthorsListView.as_view(), name='all-authors'),
    path('author/<int:pk>/', views.AuthorDetailView.as_view(), name='author'),
]
