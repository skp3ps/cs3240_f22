from django.test import TestCase
from django.urls import reverse
from .models import Course, Book
from django.contrib.auth.models import User


class ProfileEditBookPageViewTest(TestCase):
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


    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('edit_book', kwargs={'pk': self.test_bookinstance1.pk}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/accounts/login/?next=/books/' + str(self.test_bookinstance1.pk) + '/edit')



    def test_logged_in_uses_edit_right_book_populate(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('edit_book', kwargs={'pk': self.test_bookinstance1.pk}))

        # Check our user is logged in
        self.assertEqual(str(response.context['user']), 'testuser1')
        # Check that we got a response "success"
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['form'].initial['title'], 'Comp Sci')
        self.assertEqual(response.context['form'].initial['isbn'], '1234')
        self.assertEqual(response.context['form'].initial['year'], 2002)
        self.assertEqual(response.context['form'].initial['price'], 100.0)
        self.assertEqual(response.context['form'].initial['version'], 1)
        self.assertEqual(response.context['form'].initial['condition'], 'good')                
        self.assertEqual(response.context['form'].initial['image'], 'images/defaultCover.png')                        


    def test_logged_in_uses_edit_right_book_success(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('edit_book', kwargs={'pk': self.test_bookinstance1.pk}))

        # Check our user is logged in
        self.assertEqual(str(response.context['user']), 'testuser1')
        # Check that we got a response "success"
        response = self.client.post(reverse('edit_book', kwargs={'pk':self.test_bookinstance1.pk,}), {'title': 'Comp Sci', 'isbn': '1234', 'year': 2003, 'price': 100.0, 'version': 1, 'condition': 'GOOD', 'image': 'images/defaultCover.png'}, follow=True)
        self.assertRedirects(response, reverse('profile'))

        # response = self.client.post(reverse('renew-book-librarian', kwargs={'pk':self.test_bookinstance1.pk,}), {'renewal_date':valid_date_in_future}, follow=True)
        # Check we used correct booklist after deletion

        self.assertEqual(str(response.context['user']), 'testuser1')
        self.assertTemplateUsed(response, 'website/profile.html')       
        self.assertEqual(response.context['user'].book_set.count(), 2)


        self.assertEqual(response.context['user'].book_set.get(id=1).title, 'Comp Sci')
        self.assertEqual(response.context['user'].book_set.get(id=1).isbn, '1234')
        self.assertEqual(response.context['user'].book_set.get(id=1).year, 2003)
        self.assertEqual(response.context['user'].book_set.get(id=1).price, 100.0)
        self.assertEqual(response.context['user'].book_set.get(id=1).version, 1)
        self.assertEqual(response.context['user'].book_set.get(id=1).condition, 'GOOD')




