from django.urls import path, re_path

# ./catalog/
from . import views

urlpatterns = [
    path('', views.load_index, name='index_url'),
    path('books_old_way/', views.load_books_old_way, name='books_url_old'),
    path('books/', views.BookListView.as_view(), name='books_url'),
    re_path(r'^book/b/(?P<book_date>[0-9]{4}-[0-9]{2}-[0-9]{2})$', views.BookDetailViewDate.as_view(), name='book-detail'),
    re_path(r'^book/(?:page-)?(?P<book_id>\d+)$', views.BookDetailView.as_view(), name='book-detail'),

    path('authors/', views.AuthorListView.as_view(), name='authors_url'),
    path('author/<int:id>', views.AuthorDetailView.as_view(), name='author-detail'),

]
urlpatterns += [
    path('mybooks/', views.LoanedBooksByUserListView.as_view(), name='my-borrowed'),
    path('borrowed/', views.loaned_books_all_ListView, name='all-borrowed'),  # Added for challenge
]


# Add URLConf for librarian to renew a book.
urlpatterns += [
    path('book/<uuid:pk>/renew/', views.renew_book_librarian, name='renew-book-librarian'),
]

urlpatterns += [
    path('author/create/', views.AuthorCreate.as_view(), name='author-create'),
    path('author/<int:pk>/update/', views.AuthorUpdate.as_view(), name='author-update'),
    path('author/<int:pk>/delete/', views.AuthorDelete.as_view(), name='author-delete'),
]

urlpatterns += [
    path('book/create/', views.BookCreate.as_view(), name='book-create'),
    path('book/<int:pk>/update/', views.BookUpdate.as_view(), name='book-update'),
    path('book/<int:pk>/delete/', views.BookDelete.as_view(), name='book-delete'),
]
