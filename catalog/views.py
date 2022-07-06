from django.shortcuts import render
from .models import Author, Book, BookInstance
from django.views import generic


def home(request):
    num_authors = Author.objects.all().count()
    num_books = Book.objects.all().count()
    num_available = BookInstance.objects.filter(status__exact='a').count()
    num_copies = BookInstance.objects.all().count()
    context = {
        'num_authors': num_authors,
        'num_books': num_books,
        'num_available': num_available,
        'num_copies': num_copies,
    }
    return render(request, 'catalog/home.html', context)


class AllBooksListView(generic.ListView):
    model = Book
    template_name = "catalog/all_books.html"

    ordering = ['-added_date']


class BookDetailView(generic.DetailView):
    model = Book
    template_name = "catalog/book.html"


class AllAuthorsListView(generic.ListView):
    model = Author
    template_name = "catalog/all_authors.html"


class AuthorDetailView(generic.DetailView):
    model = Author
    template_name = "catalog/author.html"
