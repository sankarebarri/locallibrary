from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('borrowed-books/', views.AllBorrowedBooksListView.as_view(), name='borrowed-books'),
    path('borrowed-users/', views.AllBorrowedUsersListView.as_view(), name='borrowed-users'),
    path('renew-book/<int:pk>/renew/', views.renew_book_librarian, name='renew-book'),
    path('add-book/', views.AddNewBook.as_view(), name='add-book'),
    path('add-author/', views.AddNewAuthor.as_view(), name='add-author'),
    path('registration/', views.registration, name='registration'),
]
