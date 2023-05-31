from django.shortcuts import render
from.models import Author,Book,BookInstance,Genre,Language
from django.views import generic

def index(request):
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    num_authors = Author.objects.count()
    num_genres = Genre.objects.all().count()
    particular_word = Book.objects.filter(summary__icontains='theme').count()
    num_visits = request.session.get('num_visits',0)
    request.session['num_visits'] = num_visits + 1
    
    context = {
        'num_books':num_books,
        'num_instances':num_instances,
        'num_instances_available':num_instances_available,
        'num_authors':num_authors,
        'num_genres':num_genres,
        'particular_word':particular_word,
        'num_visits':num_visits,
    }
    return render(request,'catalog/index.html',context=context)

class BookListView(generic.ListView):
    model = Book
    paginate_by = 3
    
class BookDetailView(generic.DetailView):
    model = Book
    
class AuthorListView(generic.ListView):
    model = Author
    paginate_by = 3
    
class AuthorDetailView(generic.DetailView):
    model = Author