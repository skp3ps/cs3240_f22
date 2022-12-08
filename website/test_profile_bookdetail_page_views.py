from django.test import TestCase
from django.urls import reverse
from .models import Course, Book
from django.contrib.auth.models import User
import uuid

class ProfileBookDetailPageViewTest(TestCase):
    def setUp(self):
        # Create two users
        test_user1 = User.objects.create_user(username='testuser1', password='1X<ISRUkw+tuK')
        test_user2 = User.objects.create_user(username='testuser2', password='2HJ1vRV0Z&3iD')

        test_user1.save()
        test_user2.save()        


        # Create books
        course = Course.objects.create(subject='CS', semester_code=1228, course_number=15991, course_section='001', catalog_number='3240', instructor_name='Paul McBurney',instructor_email='pm8fc@virginia.edu', description='Computer Science', 
        units='cs class units', component='abcd', class_capacity=100, wait_list=140, wait_cap=50, enrollment_total=500, enrollment_available=500, meetings_days='TF',
        meetings_start_time='2022-01-01', meetings_end_time='2022-12-31', facility_description='good facility')
        # user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
        self.test_bookinstance1 = Book.objects.create(seller=test_user1, course=course, title='Comp Sci', isbn='1234', year=2002, price=100.0, version=1, condition='good')
        self.test_bookinstance2 = Book.objects.create(seller=test_user1, course=course, title='Introduction to Database', isbn='2345', year=2012, price=110.0, version=1, condition='good')        

    def test_view_url_exists_at_desired_location(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get('/books/' + str(self.test_bookinstance1.pk))
        self.assertEqual(response.status_code, 200)
    
    
    def test_ok_if_not_logged_in(self):
        response = self.client.get(reverse('book_detail', kwargs={'pk': self.test_bookinstance1.pk}))
        self.assertEqual(response.status_code, 200)


    
    def test_logged_in_uses_correct_template(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('book_detail', kwargs={'pk': self.test_bookinstance1.pk}))

        # Check our user is logged in
        self.assertEqual(str(response.context['user']), 'testuser1')
        # Check that we got a response "success"
        self.assertEqual(response.status_code, 200)

        # Check we used correct template
        self.assertTemplateUsed(response, 'website/book_detail.html')       
        #later on change to aref      
        # self.assertContains(response, '<a href="%s">Edit Book</a>')
        self.assertContains(response, 'Edit Book')        
        self.assertContains(response, 'Delete Book')        



    def test_logged_in_uses_correct_template_not_sellor(self):
        login = self.client.login(username='testuser2', password='2HJ1vRV0Z&3iD')
        response = self.client.get(reverse('book_detail', kwargs={'pk': self.test_bookinstance1.pk}))

        # Check our user is logged in
        self.assertEqual(str(response.context['user']), 'testuser2')
        # Check that we got a response "success"
        self.assertEqual(response.status_code, 200)

        # Check we used correct template
        self.assertTemplateUsed(response, 'website/book_detail.html') 
        self.assertContains(response, 'Contact Seller')        
        self.assertContains(response, 'Favorite Book')        


    def test_HTTP404_for_invalid_book_if_logged_in(self):
        login = self.client.login(username='testuser1', password='2HJ1vRV0Z&3iD')
        response = self.client.get(reverse('book_detail', kwargs={'pk': self.test_bookinstance1.pk + 10}))
        self.assertEqual(response.status_code, 404)





    def test_logged_in_uses_correct_booklist(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('book_detail', kwargs={'pk': self.test_bookinstance1.pk}))

        # Check that we got a response "success"
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['book'].title, 'Comp Sci')
        self.assertEqual(response.context['book'].isbn, '1234')
        self.assertEqual(response.context['book'].year, 2002)
        self.assertEqual(response.context['book'].price, 100.0)
        self.assertEqual(response.context['book'].version, 1)
        self.assertEqual(response.context['book'].condition, 'good')






