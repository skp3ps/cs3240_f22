from django.test import TestCase
from django.urls import reverse
from .models import Course, Book
from django.contrib.auth.models import User

class HomePageViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create books

        course1 = Course.objects.create(subject='CS', semester_code=1228, course_number=15991, course_section='001', catalog_number='3240', instructor_name='Paul McBurney',instructor_email='pm8fc@virginia.edu', description='Computer Science', 
        units='cs class units', component='abcd', class_capacity=100, wait_list=140, wait_cap=50, enrollment_total=500, enrollment_available=500, meetings_days='TF',
        meetings_start_time='2022-01-01', meetings_end_time='2022-12-31', facility_description='good facility')
        # user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
        course2 = Course.objects.create(subject='WGS', semester_code=1228, course_number=13512, course_section='001', catalog_number='7500', instructor_name='Tiffany King',instructor_email='tjk9b@virginia.edu', description='WGS', 
        units='WGS class units', component='abcd', class_capacity=100, wait_list=140, wait_cap=50, enrollment_total=500, enrollment_available=500, meetings_days='TF',
        meetings_start_time='2022-01-01', meetings_end_time='2022-12-31', facility_description='good facility')

        test_user1 = User.objects.create_user(username='testuser1', password='1X<ISRUkw+tuK')
        test_user2 = User.objects.create_user(username='testuser2', password='2HJ1vRV0Z&3iD')

        test_user1.save()
        test_user2.save()        
        Book.objects.create(seller=test_user1, course=course1, title='Comp Sci', isbn='1234', year=2002, price=100.0, version=1, condition='good')
        Book.objects.create(seller=test_user1, course=course1, title='Introduction to Database', isbn='2345', year=2012, price=110.0, version=1, condition='good')        
        Book.objects.create(seller=test_user2, course=course2, title='Introduction to Accounting', isbn='5678', year=2009, price=56.0, version=6, condition='good')                



    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'website/index.html')

    def test_view_login(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('home'))
        self.assertContains(response, 'Welcome, you are logged in as testuser1')



    def test_lists_all_books(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['books']), 3)
        self.assertEqual(response.context['books'][0].title, 'Comp Sci')
        self.assertEqual(response.context['books'][0].isbn, '1234')
        self.assertEqual(response.context['books'][0].year, 2002)
        self.assertEqual(response.context['books'][0].price, 100.0)
        self.assertEqual(response.context['books'][0].version, 1)
        self.assertEqual(response.context['books'][0].condition, 'good')


        self.assertEqual(response.context['books'][1].title, 'Introduction to Database')
        self.assertEqual(response.context['books'][1].isbn, '2345')
        self.assertEqual(response.context['books'][1].year, 2012)
        self.assertEqual(response.context['books'][1].price, 110.0)
        self.assertEqual(response.context['books'][1].version, 1)
        self.assertEqual(response.context['books'][1].condition, 'good')

        self.assertEqual(response.context['books'][2].title, 'Introduction to Accounting')
        self.assertEqual(response.context['books'][2].isbn, '5678')
        self.assertEqual(response.context['books'][2].year, 2009)
        self.assertEqual(response.context['books'][2].price, 56.0)
        self.assertEqual(response.context['books'][2].version, 6)
        self.assertEqual(response.context['books'][2].condition, 'good')



    def test_no_books(self):
        #clear the books in DB
        Course.objects.all().delete()
        Book.objects.all().delete()
        print("After deleting, list of courses in DB: " + str(Course.objects.count()))
        print("After deleting, list of books in DB: " + str(Book.objects.count()))
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'There are no books for sale')

