from django.contrib import admin
from .models import Author, Genre, Language, Book, BookInstance

class BookInline(admin.TabularInline):
    model = Book
    fields = ['title', 'genre', 'book_id']


#admin.site.register(Author)
@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "date_of_birth", "date_of_death")
    fields = [('last_name', 'first_name'),("date_of_birth", "date_of_death")]
    inlines = [BookInline]
admin.site.register(Genre)
admin.site.register(Language)

class BookInstanceInline(admin.TabularInline):
    model = BookInstance

#admin.site.register(Book)
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "display_genre", "book_id")
    inlines = [BookInstanceInline]
    list_filter = ('author', 'genre')
    prepopulated_fields = {"slug": ("title",)}


#admin.site.register(BookInstance)
@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_filter = ['status']
