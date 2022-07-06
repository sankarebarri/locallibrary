from django.db import models
import uuid
from django.urls import reverse
from datetime import date
from django.contrib.auth.models import User
from django.utils.text import slugify

class Author(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    date_of_birth = models.DateField('DOB', null=True, blank=True)
    date_of_death = models.DateField('Died', null=True, blank=True)

    def __str__(self):
        return f'{self.first_name} - {self.last_name}'

    def get_absolute_url(self):
        return reverse('author', args=[str(self.id)])

class Genre(models.Model):
    name = models.CharField(max_length=20, help_text='ex: Sci-FI')

    def __str__(self):
        return self.name

class Language(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class Book(models.Model):
    book_id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='unique ID for this book')
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True)
    isbn = models.IntegerField('ISBN', unique=True, help_text='13 unique integers')
    imprint = models.CharField(max_length=50)
    published_date = models.DateField()
    added_date = models.DateField(auto_now_add=True)
    summary = models.TextField(max_length=1000, help_text='Enter the book summary here')
    genre = models.ManyToManyField(Genre)
    language = models.ForeignKey(Language, on_delete=models.SET_NULL, null=True)
    slug = models.SlugField(null=True, unique=True, blank=True)

    def display_genre(self):
        return ", ".join(genre.name for genre in self.genre.all())

    def get_absolute_url(self):
        return reverse('book', kwargs={'slug': self.slug})

    def __str__(self):
        return f'{self.title} --> {self.author}'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)
class BookInstance(models.Model):
    book = models.ForeignKey(Book, on_delete=models.RESTRICT, null=True)
    due_back = models.DateField(null=True, blank=True)
    LOAN_STATUS = (
        ('o', 'On loan'),
        ('m', 'Maintenance'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )
    status = models.CharField(choices=LOAN_STATUS, max_length=1, blank=True,
                                default='m', help_text='Book availability'
    )
    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    @property
    def is_overdue(self):
        return bool(self.due_back and date.today() > self.due_back)

    class Meta:
        permissions = (('can_mark_returned', 'Set book as returned'), ('can_see_borrower', 'Can see book borrower'),)

    def __str__(self):
        return f'{self.book} --> {self.book.book_id}'
