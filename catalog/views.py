from django.shortcuts import render
from.models import Author,Book,BookInstance,Genre,Language
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from django.contrib.auth.decorators import login_required,permission_required

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
    
class LoanedBooksByUserListView(LoginRequiredMixin,generic.ListView):
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10
    def get_queryset(self):
        return(BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back'))
    
class LoanedBooksAllListView(PermissionRequiredMixin,generic.ListView):
    model = BookInstance
    permission_required = 'catalog.can_mark_returned'
    template_name = 'catalog/bookinstance_list_borrowed_all.html'
    paginate_by = 10
    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='o').order_by('due_back')
    
@login_required
@permission_required('catalog.can_mark_returned',raise_exception=True)
def renew_book_librarian(request,pk):
    return render(request,'catalog/book_renew_librarian.html')