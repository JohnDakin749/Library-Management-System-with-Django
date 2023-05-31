from django.contrib import admin
from.models import Author,Book,BookInstance,Language,Genre

#admin.site.register(Author)
class BooksInline(admin.TabularInline):
    model = Book
    extra = 0
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name','first_name','date_of_birth','date_of_death')
    #fields =[('first_name','last_name'),('date_of_birth','date_of_death')]
    fieldsets = (
        ('Author Names',{
            'fields':('last_name','first_name')
        }),
        ('Life Time',{
            'fields':('date_of_birth','date_of_death')
        }),
    )
    inlines = [BooksInline]
admin.site.register(Author,AuthorAdmin)
#admin.site.register(Book)
class BooksInstanceInline(admin.TabularInline):
    model = BookInstance
    extra = 0
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title','author','display_genre')
    fieldsets = (
        ('Book Information',{
            'fields':('title','author','summary','genre','language')
        }),
    )
    inlines = [BooksInstanceInline]

#admin.site.register(BookInstance)
@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('status','due_back','id')
    list_filter = ('status','due_back')
    fieldsets = (
        ('Information',{
            'fields':('book','imprint','id')
        }),
        ('Availability',{
            'fields':('status','due_back')
        }),
    )
    
#admin.site.register(Language)
@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Edit/Add Book Language',{
            'fields':('name',)
        }),
    )
#admin.site.register(Genre)
@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Edit/Add Book Genre',{
            'fields':('name',)
        }),
    )