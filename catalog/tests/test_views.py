from django.test import TestCase
from catalog.models import Author
from django.urls import reverse
import datetime
from django.utils import timezone
from catalog.models import BookInstance,Book,Genre,Language
from django.contrib.auth.models import User
from django.contrib.auth.models import Permission
import uuid
class AuthorListViewTest(TestCase):
    
    @classmethod
    def setUpTestData(cls):
        num_of_authors = 13
        for author_id in range(num_of_authors):
            Author.objects.create(first_name='Christian {0}'.format(author_id),last_name='Surname {0}'.format(author_id))
            
    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/catalog/authors')
        self.assertEqual(response.status_code, 200)
        
    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('authors'))
        self.assertEqual(response.status_code, 200)
        
    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('authors'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,'catalog/author_list.html')
        
    def test_pagination_is_ten(self):
        response = self.client.get(reverse('authors'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] is True)
        self.assertEqual(len(response.context['author_list']), 10)
        
    def test_list_all_authors(self):
        response = self.client.get(reverse('authors')+'page=2')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] is True)
        self.assertEqual(len(response.context['author_list']), 3)
        
# =====================================Another Test=====================================================#

class LoanedBookInstanceByUserListViewTest(TestCase):
    
    def setUp(self):
        test_user1 = User.objects.create_user(username='testuser1', password='1x<ISRUKw+tuK')
        test_user2 = User.objects.create_user(username='testuser2', password='2HJ1vRV0Z&3iD')
        
        test_user1.save()
        test_user2.save()
        
        test_author = Author.objects.create(first_name='John', last_name='Dakin')
        test_genre = Genre.objects.create(name='Fantasy')
        test_language = Language.objects.create(name='English')
        test_book = Book.objects.create(
            title = 'Book Title',
            summary = 'My book summary',
            isbn = 'ABCDEFG',
            author = test_author,
            Language = test_language,
        )
        
        genre_objects_for_book = Genre.objects.all()
        test_book.genre.set(genre_objects_for_book)
        test_book.save()
        
        num_of_book_copies = 30
        for book_copy in range(num_of_book_copies):
            return_date = timezone.now() + datetime.timedelta(days=book_copy % 5)
            if book_copy % 2:
                the_borrower = test_user1
            else:
                the_borrower = test_user2
            status = 'm'
            BookInstance.objects.create(book=test_book,imprint='Unlikely Imprint, 2016', due_back=return_date,borrower=the_borrower,status=status)
            
    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('my-borrowed'))
        self.assertRedirects(response,'/accounts/login/?next=/catalog/mybooks/')
        
    def test_logged_in_user_correct_template(self):
        login = self.client.login(username='testuser1', password='1X<ISRUKw+tuK')
        response = self.client.get(reverse('my-borrowed'))
        
        self.assertEqual(str(response.context['user']), 'testuser1')
        
        self.assertEqual(response.status_code, 200)
        
        self.assertTemplateUsed(response,'catalog/bookinstance_list_borrowed_user.html')
        
    def test_only_borrowed_books_in_list(self):
        login = self.client.login(username='testuser1',password='1X<ISRUKw+tuK')
        response = self.client.get(reverse('my-borrowed'))
        
        self.assertEqual(str(response.context['user']),'testuser1')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('bookinstance_list' in response.context)
        self.assertEqual(len(response.context['bookinstance_list']),0)
        
        get_ten_books = BookInstance.objects.all()[:10]
        
        for copy in get_ten_books:
            copy.status = 'o'
            copy.save()
            
        response = self.client.get(reverse('my-borrowed'))
        self.assertEqual(str(response.context['user']),'testuser1')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('bookinstance_list' in response.context)
        
        for bookitem in response.context['bookinstance_list']:
            self.assertEqual(response.context['user'], bookitem.borrower)
            self.assertEqual(bookitem.status, 'o')
            
    def test_pages_psginated_to_ten(self):
        
        for copy in BookInstance.objects.all():
            copy.status = 'o'
            copy.save()
            
        login = self.client.login(username='testuser1',password='1X<ISRUKw+tuK')
        response = self.client.get(reverse('my-borrowed'))
        
        self.assertEqual(str(response.context['user']),'testuser1')
        self.assertEqual(response.status_code, 200)
        
        self.assertEqual(len(response.context['bookinstance_list']),10)
        
    def test_pages_ordered_by_due_date(self):
        
        for copy in BookInstance.objects.all():
            copy.status = 'o'
            copy.save()
            
        login = self.client.login(username='testuser1', password='1X<ISRUKw+tuK')
        response = self.client.get(reverse('my-borrowed'))
        
        self.assertEqual(str(response.context['user']), 'testuser1')
        self.assertEqual(response.status_code, 200)
        
        self.assertEqual(len(response.context['bookinstance_list']),10)
        
        last_date = 0
        for copy in response.context['bookinstance_list']:
            if last_date == 0:
                last_date = copy.due_back
            else:
                self.assertTrue(last_date <= copy.due_back)
                
                
# =========================Permissions Test===========================================================#

class RenewBookInstancesViewTest(TestCase):
    
    def setUp(self):
        
        test_user1 = User.objects.create_user(username='testuser1',password='1X<ISRUKw+tuK')
        test_user1.save()
        
        test_user2 = User.objects.create_user(username='testuser2',password='2HJIvRVOZ&3iD')
        test_user2.save()
        permission = Permission.objects.get(name='Set book as returned')
        test_user2.user_permissions.add(permission)
        test_user1.save()
        
        test_author = Author.objects.create(first_name='John', last_name='Dakin')
        test_genre = Genre.objects.create(name='Fantasy')
        test_language = Language.objects.create(name='English')
        test_book = Book.objects.create(title='Book Tite', summary='My book summary', isbn='ABCDEFG', author=test_author,language=test_language,)
        
        genre_objects_for_book = Genre.objects.all()
        test_book.genre.set(genre_objects_for_book)
        test_book.save()
        
        return_date = datetime.date.today() + datetime.timedelta(days=5)
        self.test_bookinstance1 = BookInstance.objects.create(
            book=test_book,
            imprint = 'Unlikely  Imprint, 2016',
            due_back = return_date,
            borrower = test_user1,
            status = 'o'
        )
        
        return_date = datetime.date.today() + datetime.timedelta(days=5)
        self.test_bookinstance2 = BookInstance.objects.create(
            book=test_book,
            imprint = 'Unlikely  Imprint, 2016',
            due_back = return_date,
            borrower = test_user2,
            status = 'o'
        )
        
    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('renew-book-librarian', kwargs={'pk':self.bookinstance1.pk}))
        self.assertEqual(response.status_code, 403)
        
    def test_forbidden_if_logged_in_but_not_correct_permission(self):
        login = self.client.login(username='testuser1', password='1X<ISRUKw+tuK')
        response = self.client.get(reverse('renew-book-librarian', kwargs={'pk':self.bookinstance1.pk}))
        self.assertEqual(response.status_code, 403)
        
    def test_forbidden_if_logged_in_with_permission_borrowed_book(self):
        login = self.client.login(username='testuser2', password='2HJIvRVOZ&3iD')
        response = self.client.get(reverse('renew-book-librarian', kwargs={'pk':self.bookinstance1.pk}))
        self.assertEqual(response.status_code, 200)
        
    def test_user_correct_template(self):
        login = self.client.login(username='testuser2', password='2HJIvRVOZ&3iD')
        response = self.client.get(reverse('renew-book-librarian', kwargs={'pk':self.bookinstance1.pk}))
        self.assertEqual(response.status_code, 200)
        
        self.assertTemplate(response,'catalog/book_renew_librarian.html')
        
    def test_form_renewal_date_initially_has_date_three_weeks_in_future(self):
        login = self.client.login(username='testuser2', password='2HJIvRVOZ&3iD')
        response = self.client.get(reverse('renew-book-librarian', kwargs={'pk':self.bookinstance1.pk}))
        self.assertEqual(response.status_code, 200)
        
        date_3_weeks_in_future = datetime.date.today() + datetime.timedelta(weeks=3)
        self.assertEqual(response.status_code,200)
        date_3_weeks_in_future = datetime.date.today() + datetime.timedelta(weeks=3)
        self.assertEqual(response.context['form'].initial['renewal_date'],date_3_weeks_in_future)
        
    def test_form_invalid_renewal_date_past(self):
        login = self.client.login(usename='testuser2',password='2HJIvRVOZ&3iD')
        
        date_in_past = datetime.date.today() - datetime.timedelta(weeks=1)
        response = self.client.post(reverse('renewal-book-librarian', kwargs={'pk':self.test_bookinstance1.pk}),
                                    {'renewal_date':date_in_past})
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form','renewal_date','invalid date - renewal in past')
        
    def test_form_invalid_renewal_date_future(self):
        login = self.client.login(usename='testuser2',password='2HJIvRVOZ&3iD')
        
        date_in_past = datetime.date.today() + datetime.timedelta(weeks=5)
        response = self.client.post(reverse('renewal-book-librarian', kwargs={'pk':self.test_bookinstance1.pk}),
                                    {'renewal_date':date_in_past})
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form','renewal_date','invalid date - renewal more than 4 weeks ahead')
        
    def test_redirects_to_all_borrowed_book_list_on_success(self):
        login = self.client.login(usename='testuser2',password='2HJIvRVOZ&3iD')
        
        valid_date_in_future = datetime.date.today() + datetime.timedelta(weeks=2)
        response = self.client.post(reverse('renew-book-librarian',kwargs={'pk':self.test_bookinstance1.pk}),
                                    {'renewal_date':valid_date_in_future})
        self.assertRedirects(response,reverse('all-borrowed'))
        
    def test_HTTP404_for_invalid_book_if_logged_in(self):
        test_uuid = uuid.uuid4()
        login = self.client.login(username='testuser2',password='2HJIvRVOZ&3iD')
        response = self.client.get(reverse('renew-book-librarian',kwargs={'pk':test_uuid}))
        self.assertEqual(response.status_code, 404)
        
class AuthorCreateViewTest(TestCase):
    
    def setUp(self):
        test_user1 = User.objects.create_user(username='testuser1', password='1X<ISRUKw+tuK')
        test_user2 = User.objects.create_user(username='testuser2', password='2HJIvRVOZ&3iD')
        
        test_user1.save()
        test_user2.save()
        
        permission = Permission.objects.get(name='Set book as returned')
        test_user2.user_permissions.add(permission)
        test_user2.save()
        
        test_author = Author.objects.create(first_name='John',last_name='Smith')
        
    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('author-create'))
        self.assertRedirects(response,'/accounts/login/?next=/catalog/author/create/')
        
    def test_forbidden_if_logged_in_but_not_correct_permission(self):
        login = self.client.login(username='testuser1',password='1X<ISRUKw+tuK')
        response = self.client.get(reverse('author-create'))
        self.assertEqual(response.status_code, 403)
        
    def test_forbidden_if_logged_in_with_permission(self):
        login = self.client.login(username='testuser2',password='2HJIvRVOZ&3iD')
        response = self.client.get(reverse('author-create'))
        self.assertEqual(response.status_code, 200)
        
    def test_user_correct_template(self):
        login = self.client.login(username='testuser2',password='2HJIvRVOZ&3iD')
        response = self.client.get(reverse('author-create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'catalog/author_form.html')
        
    def test_form_date_of_death_initially_set_to_expected_date(self):
        login = self.client.login(username='testuser2',password='2HJIvRVOZ&3iD')
        response = self.client.get(reverse('author-create'))
        self.assertEqual(response.status_code, 200)
        
        expected_initial_date = datetime.date(2020,6,11)
        response_date = response.context['form'].initial['date_of_death']
        response_date = datetime.datetime.strptime(response_date,"%d%m%Y").date()
        self.assertEqual(response_date,expected_initial_date)
        
    def test_redirects_to_detail_view_on_success(self):
        login = self.client.login(username='testuser2',password='2HJIvRVOZ&3iD')
        response = self.client.post(reverse('author-create'),
                                    {'first_name':'Christian Name','last_name':'Surname'})
        self.assertEqual(response.status_code, 200)
        
        self.assertEqual(response.status_code,302)
        self.assertTrue(response.url.startswith('/catalog/author/'))