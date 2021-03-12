import datetime

from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.views.generic import CreateView, UpdateView, DeleteView

from .forms import RenewBookForm, RenewBookModelForm
from .models import Book, BookInstance, Author, Genre


def catalogWelcome():
    return HttpResponse("<h2>This will be catalog</h2>")


@login_required(redirect_field_name='redirect_to', login_url='/accounts/login/')
def load_index(request):
    """View function for home page of site."""

    request.session['num_visits'] = request.session.get('num_visits', 0) + 1

    num_authors = Author.objects.count()

    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.count()  # no need of all()

    # Available books (status = 'a' OR available)
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    num_genres_science = Genre.objects.filter(name__icontains='science').count()

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_genres_science': num_genres_science,
    }
    # red
    return render(request, 'index.html', context=context)


@login_required
def load_books_old_way(request):
    num_books = Book.objects.count()
    books = ', '.join(book.title for book in Book.objects.all())
    context = {
        'num_books': num_books,
        'books': books,
    }
    return render(request, 'books.html', context=context)


class BookListView(LoginRequiredMixin, generic.ListView):
    model = Book
    context_object_name = 'my_book_list'  # override the name for TEMPLATE-variable
    template_name = 'books/book_list.html'
    paginate_by = 3
    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'

    # queryset = Book.objects.all()
    # def get_queryset(self):  # getting only this much query
    #     return self.model.objects.filter(title__icontains='war')[:5]  # top 5

    def get_context_data(self, **kwargs):
        context = super(BookListView, self).get_context_data(**kwargs)
        context['num_books'] = Book.objects.count()
        return context

    # in total we are passing template-name, num_books, context_object_name along with other data


class BookDetailView(LoginRequiredMixin,
                     generic.DetailView):  # detail view will identify utl variables and pass automatically
    model = Book
    template_name = 'books/book_model_details.htm'
    context_object_name = 'book'

    #  but by default it only get url-variable passed in <pk> so overriding slug/pk
    pk_url_kwarg = "book_id"

    # def get_object(self, queryset=None):
    #     return get_object_or_404(Book, re)
    login_url = '/login/'  # if not logged-in then it will redirect to /login
    redirect_field_name = 'redirect_to'  # in place of ?next=

    def get_context_data(self, **kwargs):
        print(kwargs)
        context = super(BookDetailView, self).get_context_data(**kwargs)
        context['num_books'] = Book.objects.count()
        return context


# def book_detail_view(request, pk):
#     try:
#         book = Book.objects.all().get(pk=pk)
#     except Book.DoesNotExist:
#         raise Http404('Book with pKey:{pk} does not exist')
#     return render(request=request, template_name='books/book_model_details.htm', context={'book': book})


class BookDetailViewDate(generic.DetailView):  # detail view will identify utl variables and pass automatically
    model = Book
    template_name = 'books/book_model_details.htm'
    context_object_name = 'book'

    #  but by default it only get url-variable passed in <pk> so overriding slug/pk
    pk_url_kwarg = "book_date"

    def get_object(self, queryset=None):
        return Book.objects.filter(release__gte=self.pk_url_kwarg)

    def get_context_data(self, **kwargs):
        print(kwargs)
        context = super(BookDetailView, self).get_context_data(**kwargs)
        context['num_books'] = Book.objects.count()
        return context


class AuthorListView(generic.ListView):
    model = Author
    template_name = 'authors/authors_list.html'
    context_object_name = 'my_authors_list'  # to be use in template
    paginate_by = 10


class AuthorDetailView(generic.DetailView):
    model = Author
    template_name = 'authors/author_details.html'
    context_object_name = 'author'
    pk_url_kwarg = 'id'  # filter applied to get particular Author Details


class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    """ List View of Loaned Books that are loaned by any user """
    model = BookInstance
    template_name = 'books/bookinstances_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__iexact='o').order_by('due_back')


@login_required(redirect_field_name='redirect_to', login_url='/accounts/login/')
@permission_required('catalog.can_view_borrowed_books',
                     raise_exception=True)  # to access it user should have this permission/s
def loaned_books_all_ListView(request):
    borrowed_books_list = BookInstance.objects.filter(status__exact='o').order_by('due_back')
    context = {
        'borrowed_books_list': borrowed_books_list,
    }
    return render(request, 'users/borrowed_books.html', context)


@login_required
@permission_required('catalog.can_mark_returned', raise_exception=True)
def renew_book_librarian(request, pk):
    book_instance = get_object_or_404(BookInstance, pk=pk)
    # try:
    #     book_instance = BookInstance.objects.get(pk=bid)
    # except BookInstance.DoesNotExist:
    #     from django.http import Http404
    #     raise Http404(f"book-instance with id: {bid} does not exist")

    if request.method == 'POST':
        print('post method')
        # create formInstance and Populate/Bind with the attached information from request
        # form = RenewBookForm(request.POST)
        form = RenewBookModelForm(request.POST)
        print('form created', form)
        # checking form valid or not
        if form.is_valid():  # check user information at server side like password,book available etc.
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            book_instance.due_back = form.cleaned_data['due_back']  # update required data finally
            book_instance.save()  # save Transaction
            return HttpResponseRedirect(reverse('all-borrowed'))  # redirect to URL after updating
        # print('form', form)
        # return render(request, "forms/book_renew_librarian.html", {'form': form})
    else:
        #  Its users first request, so create default-FORM
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        # initial data to pass while creating instance of form
        data = {'due_back': proposed_renewal_date}
        form = RenewBookModelForm(
            initial=data)  # using "initial=" assign or change content without constructor creation by user

    context = {
        'form': form,
        'book_instance': book_instance
    }
    print('before render call')
    return render(request, template_name='forms/book_renew_librarian.html', context=context)


# Generic editing views #

class AuthorCreate(PermissionRequiredMixin, CreateView):
    model = Author
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']
    initial = {'date_of_death': '11/06/2090'}
    permission_required = 'catalog.change_author'


class AuthorUpdate(PermissionRequiredMixin, UpdateView):
    # it gets the particular object based on 'pk'
    model = Author
    fields = '__all__'  # Not recommended (potential security issue if more fields added)
    permission_required = 'catalog.change_author'


class AuthorDelete(PermissionRequiredMixin, DeleteView):
    model = Author
    success_url = reverse_lazy('authors_url')
    permission_required = 'catalog.change_author'


class BookCreate(PermissionRequiredMixin, CreateView):
    model = Book
    fields = ['title', 'author', 'summary', 'isbn', 'language', 'genre', 'release']
    permission_required = 'catalog.change_book'


class BookUpdate(PermissionRequiredMixin, UpdateView):
    model = Book
    fields = '__all__'
    permission_required = 'catalog.change_book'


class BookDelete(PermissionRequiredMixin, DeleteView):
    model = Book
    success_url = reverse_lazy('books_url')
    permission_required = 'catalog.change_book'
