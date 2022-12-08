from django.test import TestCase
from django.urls import reverse
from chat.models import Room
from website.models import Course, Book
from django.contrib.auth.models import User


class ChatPageViewTest(TestCase):
    def setUp(self):
        # Create two users
        test_user1 = User.objects.create_user(username='testuser1', password='1X<ISRUkw+tuK')
        test_user2 = User.objects.create_user(username='testuser2', password='2HJ1vRV0Z&3iD')
        test_user3 = User.objects.create_user(username='testuser3', password='1X%IS&Ukw+tuK')

        test_user1.save()
        test_user2.save()        
        test_user3.save()

        # Create books
        course = Course.objects.create(subject='CS', semester_code=1228, course_number=15991, course_section='001', catalog_number='3240', instructor_name='Paul McBurney',instructor_email='pm8fc@virginia.edu', description='Computer Science', 
        units='cs class units', component='abcd', class_capacity=100, wait_list=140, wait_cap=50, enrollment_total=500, enrollment_available=500, meetings_days='TF',
        meetings_start_time='2022-01-01', meetings_end_time='2022-12-31', facility_description='good facility')
        # user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
        Book.objects.create(seller=test_user1, course=course, title='Comp Sci', isbn='1234', year=2002, price=100.0, version=1, condition='good')
        Book.objects.create(seller=test_user1, course=course, title='Introduction to Database', isbn='2345', year=2012, price=110.0, version=1, condition='good')        
        print("list of courses in DB: " + str(Course.objects.count()))
        print("list of books in DB: " + str(Book.objects.count()))


        # Create rooms
        self.room = Room.objects.create( name='room1', description='a test chat room', slug = 'abcdefghijklmn');
        self.room.participants.add(test_user1);
        self.room.participants.add(test_user2);

        self.room1 = Room.objects.create( name='room2', description='a second test chat room', slug = 'sfddsfdsfdsfsdfs');
        self.room1.participants.add(test_user1);
        self.room1.participants.add(test_user2);


        # # user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
        # Book.objects.create(seller=test_user1, course=course, title='Comp Sci', isbn='1234', year=2002, price=100.0, version=1, condition='good')
        # Book.objects.create(seller=test_user1, course=course, title='Introduction to Database', isbn='2345', year=2012, price=110.0, version=1, condition='good')        
        # print("list of courses in DB: " + str(Course.objects.count()))
        # print("list of books in DB: " + str(Book.objects.count()))


    def test_all_room_redirect_if_not_logged_in(self):
        response = self.client.get('/chat/')
        self.assertRedirects(response, '/accounts/login/?next=/chat/')

    def test_all_room_correct_template(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get('/chat/')
        self.assertEqual(response.status_code, 200)

        # Check our user is logged in
        self.assertEqual(str(response.context['user']), 'testuser1')
        # Check that we got a response "success"

        # Check we used correct template
        self.assertTemplateUsed(response, 'chat/index.html')       



    def test_all_room_url_accessible_by_name(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('all_rooms'))
        self.assertEqual(response.status_code, 200)

        # Check our user is logged in
        self.assertEqual(str(response.context['user']), 'testuser1')



    def test_token_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('token'))
        self.assertRedirects(response, '/accounts/login/?next=/chat/token')



    def test_room_detail_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('room_detail', kwargs={'slug': self.room.slug}))
        self.assertRedirects(response, '/accounts/login/?next=/chat/rooms/' + self.room.slug)



    def test_room_detail_correct_template(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('room_detail', kwargs={'slug': self.room.slug}))

        # Check our user is logged in
        self.assertEqual(str(response.context['user']), 'testuser1')
        # Check that we got a response "success"
        self.assertEqual(response.status_code, 200)

        # Check we used correct template
        self.assertTemplateUsed(response, 'chat/room_detail.html')       


    def test_log_in_no_room(self):
        login = self.client.login(username='testuser3', password='1X%IS&Ukw+tuK')
        response = self.client.get(reverse('all_rooms'))

        self.assertContains(response, 'You have not started any chats. Contact a book seller or search for a user above to start chatting!')    


    def test_log_in_rooms(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('all_rooms'))

        self.assertEqual(response.context['rooms'].count(), 2)
        self.assertEqual(response.context['rooms'].get(id=1).name, 'room1')
        self.assertEqual(response.context['rooms'].get(id=1).description, 'a test chat room')
        self.assertEqual(response.context['rooms'].get(id=1).slug, 'abcdefghijklmn')


        self.assertEqual(response.context['rooms'].get(id=2).name, 'room2')
        self.assertEqual(response.context['rooms'].get(id=2).description, 'a second test chat room')
        self.assertEqual(response.context['rooms'].get(id=2).slug, 'sfddsfdsfdsfsdfs')



    def test_log_in_rooms_search_user(self):
        login = self.client.login(username='testuser2', password='2HJ1vRV0Z&3iD')
        response = self.client.get(reverse('all_rooms'))

        response = self.client.get(reverse('all_rooms'), {'username': 'testuser1'})
        self.assertEqual(response.context['profiles'].count(), 1)
        self.assertEqual(response.context['profiles'].get(id=1).username, 'testuser1')



    def test_log_in_room_detail(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('room_detail', kwargs={'slug': self.room.slug}))

        self.assertEqual(response.context['room'].name, self.room.name)
        self.assertEqual(response.context['room'].description, self.room.description)


