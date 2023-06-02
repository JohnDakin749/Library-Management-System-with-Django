from django.urls import path
from.import views

urlpatterns=[
    path('',views.index,name='index'),
    path('books/',views.BookListView.as_view(),name='books'),
    path('book/<int:pk>',views.BookDetailView.as_view(),name='book-detail'),
    path('authors/',views.AuthorListView.as_view(),name='author'),
    path('author/<int:pk>',views.AuthorDetailView.as_view(),name='author-detail'),
    path('mybooks/',views.LoanedBooksByUserListView.as_view(),name='my-borrowed'),
    path('borrowed/',views.LoanedBooksAllListView.as_view(),name='all-borrowed'),
    path('book/<uuid:pk>/renew/',views.renew_book_librarian,name='renew-book-librarian'),
    path('author/create/',views.AuthorCreate.as_view(),name='author-create'),
    path('author/<int:pk>/update/',views.Authorupdate.as_view(),name='author-update'),
    path('author/<int:pk>/delete/',views.AuthorDelete.as_view(),name='author-delete'),
    path('book/create/',views.BookCreate.as_view(),name='book-create'),
    path('book/<int:pk>/update/',views.BookUpdate.as_view(),name='book-update'),
    path('book/<int:pk>/delete/',views.DeleteView.as_view(),name='book-delete'),
]

# The Author create,Update,Delete view are now 
# configured in the website you can hook up the 
# urls from the catalog to the base_generic.html template for use.