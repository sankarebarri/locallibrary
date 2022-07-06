import datetime
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from catalog.models import Author, Book, BookInstance
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import RenewBookForm, RegistrationForm
from django.contrib.auth.decorators import login_required, permission_required


# Create your views here.
class AllBorrowedBooksListView(LoginRequiredMixin, generic.ListView):
    model = BookInstance
    template_name = 'users/borrowed_books.html'

    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='o')



class AllBorrowedUsersListView(LoginRequiredMixin, generic.ListView):
    model = BookInstance
    template_name = 'users/borrowed_users.html'
    permission_required = 'catalog.can_see_borrower'

    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='o')

@login_required
@permission_required('catalog.can_mark_returned', raise_exception=True)
def renew_book_librarian(request, pk):
    book_instance = get_object_or_404(BookInstance, pk=pk)
    if request.method == "POST":
        form = RenewBookForm(request.POST)
        if form.is_valid():
            book_instance.due_back = form.cleaned_data['renewal_date']
            if book_instance.due_back < datetime.date.today():
                messages.info(request, 'Invalid date - renewal in past')
                return redirect("renew-book", pk=pk)
                #raise ValidationError(_())
            if book_instance.due_back > (datetime.date.today() + datetime.timedelta(weeks=4)):
                messages.info(request, 'Invalid date - renewal more than 4 weeks ahead')
                return redirect("renew-book", pk=pk)
                #raise ValidationError(_('Invalid date - renewal more than 4 weeks ahead'))
            book_instance.save()
            return redirect('borrowed-books')
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date':proposed_renewal_date})
    context = {
        'form':form,
        'book_instance':book_instance,
    }
    return render(request, 'users/book_renew_librarian.html', context)


class AddNewBook(LoginRequiredMixin, generic.CreateView):
    model = Book
    fields = "__all__"
    permission_required = 'catalog.can_mark_returned'
    template_name = 'users/add_new_book.html'


class AddNewAuthor(LoginRequiredMixin, generic.CreateView):
    model = Author
    fields = "__all__"
    template_name = "users/add_new_author.html"


def registration(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            messages.success(request, f"{username} successfully created")
            return redirect("login")
    else:
        form = RegistrationForm()
    context = {
        'form':form
    }
    return render(request, "users/registration.html", context)
