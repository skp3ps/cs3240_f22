from django.test import TestCase
from django.urls import reverse
from .models import Course, Book
from django.contrib.auth.models import User



class ProfilePageViewTest(TestCase):
    def setUp(self):
        # Create two users
        test_user1 = User.objects.create_user(username='testuser1', password='1X<ISRUkw+tuK')
        test_user2 = User.objects.create_user(username='testuser2', password='2HJ1vRV0Z&3iD')

        test_user1.save()
        test_user2.save()        


        # Create books
        self.course1 = Course.objects.create(subject='CS', semester_code=1228, course_number=15991, course_section='001', catalog_number='3240', instructor_name='Paul McBurney',instructor_email='pm8fc@virginia.edu', description='Computer Science', 
        units='cs class units', component='abcd', class_capacity=100, wait_list=140, wait_cap=50, enrollment_total=500, enrollment_available=500, meetings_days='TF',
        meetings_start_time='2022-01-01', meetings_end_time='2022-12-31', facility_description='good facility')

        self.course2 = Course.objects.create(subject='CS', semester_code=1228, course_number=15992, course_section='002', catalog_number='3240', instructor_name='Paul McBurney',instructor_email='pm8fc@virginia.edu', description='Computer Science', 
        units='cs class units', component='abcd', class_capacity=100, wait_list=140, wait_cap=50, enrollment_total=500, enrollment_available=500, meetings_days='TF',
        meetings_start_time='2022-01-01', meetings_end_time='2022-12-31', facility_description='good facility')
        # user = m
        
        for i in range(101):
           course = Course.objects.create(subject='ARCHITECTURE', semester_code=1328, course_number=15891, course_section=str(i), catalog_number='8345', class_capacity=100, wait_list=140, wait_cap=50, enrollment_total=500, enrollment_available=500, meetings_days='TF',
        meetings_start_time='2022-01-01', meetings_end_time='2022-12-31', facility_description='good facility', instructor_name='Brian Keys',instructor_email='bkeys=s@virginia.edu')


        # user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
        self.test_bookinstance1 = Book.objects.create(seller=test_user1, course=self.course1, title='Comp Sci', isbn='1234', year=2002, price=100.0, version=1, condition='good')
        self.test_bookinstance2 = Book.objects.create(seller=test_user1, course=self.course1, title='Introduction to Database', isbn='2345', year=2012, price=110.0, version=1, condition='good')        
        print("list of courses in DB: " + str(Course.objects.count()))
        print("list of books in DB: " + str(Book.objects.count()))


    def test_logged_in_uses_correct_template(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('choose_course'))

        # Check our user is logged in
        self.assertEqual(str(response.context['user']), 'testuser1')

        # Check that we got a response "success"
        self.assertEqual(response.status_code, 200)

        # Check we used correct template
        self.assertTemplateUsed(response, 'website/choose_course.html')       
        self.assertContains(response, 'Select Course')    

 


    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('choose_course'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/accounts/login/?next=/profile/choose_course')



    def test_logged_in_uses_select_course_no_match(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('choose_course'))

        # Check that we got a response "success"
        response = self.client.get(reverse('choose_course'), {'subject': 'AAA'})
        self.assertContains(response, 'No courses match your selections.')    


    def test_logged_in_uses_select_course_single_match(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('choose_course'))

        # Check that we got a response "success"
        response = self.client.get(reverse('choose_course'), {'subject': 'CS'})
        self.assertContains(response, 'Courses')    
        response = self.client.post(reverse('choose_course'), {'course': self.course1.pk}, follow=True)
        self.assertTemplateUsed(response, 'website/add_book.html')       




    def test_logged_in_uses_select_course_greater_than_100_match(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('choose_course'))

        # Check our user is logged in
        self.assertEqual(str(response.context['user']), 'testuser1')
        # Check that we got a response "success"
        response = self.client.get(reverse('choose_course'), {'subject': 'ARCHITECTURE'})
        # self.assertContains(response, 'Please enter additional search criteria to see available courses.')    
        # self.assertContains(response, 'Please enter additional search criteria to see available courses.')            
        self.assertEqual(response.context['error_message'], 'Too many courses match your selections. Please enter additional search criteria to see available courses.')


    def test_logged_in_uses_select_course_NO_match(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('choose_course'))

        # Check our user is logged in
        self.assertEqual(str(response.context['user']), 'testuser1')
        # Check that we got a response "success"
        response = self.client.get(reverse('choose_course'), {'subject': 'ARCHITECTUR'})
        # self.assertContains(response, 'Please enter additional search criteria to see available courses.')    
        # self.assertContains(response, 'Please enter additional search criteria to see available courses.')            
        self.assertEqual(response.context['error_message'], 'No courses match your selections.')




    def test_logged_in_uses_select_course_and_add(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('choose_course'))

        # Check that we got a response "success"
        response = self.client.get(reverse('choose_course'), {'subject': 'CS'})
        self.assertContains(response, 'Courses')    
        response = self.client.post(reverse('choose_course'), {'course': self.course1.pk}, follow=True)
        # print ("pk of course 1: " + str(self.course1.pk))
        response = self.client.post(reverse('add_book', kwargs={'pk': self.course1.pk}), { 'title': 'Comp Sci', 'isbn': '1234', 'year': 2003, 'price': 100.0, 'version': 1, 'condition': 'GOOD', 'image': 'path/static/website/defaultCover.png'}, follow=True)


        # Check we used correct booklist after add

        self.assertEqual(str(response.context['user']), 'testuser1')
        self.assertTemplateUsed(response, 'website/profile.html')       
        self.assertEqual(response.context['user'].book_set.count(), 3)


        self.assertEqual(response.context['user'].book_set.get(id=3).title, 'Comp Sci')
        self.assertEqual(response.context['user'].book_set.get(id=3).isbn, '1234')
        self.assertEqual(response.context['user'].book_set.get(id=3).year, 2003)
        self.assertEqual(response.context['user'].book_set.get(id=3).price, 100.0)
        self.assertEqual(response.context['user'].book_set.get(id=3).version, 1)
        self.assertEqual(response.context['user'].book_set.get(id=3).condition, 'GOOD')


