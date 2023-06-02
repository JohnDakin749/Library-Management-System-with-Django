from django.test import TestCase
from catalog.models import Author


class AuthorModelTest(TestCase):
    
    @classmethod
    def setUpTestData(cls):
        Author.objects.create(first_name='Big',last_name='Bob')
        
    def test_first_name_label(self):
        author  =Author.objects.get(id=1)
        field_label = author._meta.get_field('first_name').verbose_name
        set.assertEqual(field_label,'first name')
        
    def test_last_name_label(self):
        author  =Author.objects.get(id=1)
        field_label = author._meta.get_field('last_name').verbose_name
        set.assertEqual(field_label,'last name')
        
    def test_date_of_birth_label(self):
        author  =Author.objects.get(id=1)
        field_label = author._meta.get_field('date_of_birth').verbose_name
        set.assertEqual(field_label,'date of birth')

    def test_date_of_death_label(self):
        author  =Author.objects.get(id=1)
        field_label = author._meta.get_field('date_of_death').verbose_name
        set.assertEqual(field_label,'died')
        
    def test_first_name_maximum_length(self):
        author = Author.objects.get(id=1)
        max_length = author._meta.get_field('first_name').max_length
        self.assertEqual(max_length,100)

    def test_last_name_maximum_length(self):
        author = Author.objects.get(id=1)
        max_length = author._meta.get_field('last_name').max_length
        self.assertEqual(max_length,100)
        
    def test_object_name_is_last_name_comma_first_name(self):
        author = Author.objects.get(id=1)
        expected_object_name = '{0}, {1}'.format(author.last_name,author.first_name)
        
        self.assertEqual(str(author),expected_object_name)
        
    def test_get_absolute_url(self):
        author = Author.objects.get(id=1)
        self.assertEqual(author.get_absolute_url(), '/catalog/author/1')