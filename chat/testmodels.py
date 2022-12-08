from django.db import models
from django.test import TestCase
from chat.models import Room
from django.contrib.auth.models import User


# Create your tests here.
class RoomModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        user = User.objects.create()
        room = Room.objects.create( name='room1', description='a test chat room', slug = 'abcdefghijklmn');



    def test_room_name_label(self):
        room = Room.objects.get(id=1)
        field_label = room._meta.get_field('name').verbose_name
        self.assertEqual(field_label, 'name')


    def test_room_description_label(self):
        room = Room.objects.get(id=1)
        field_label = room._meta.get_field('description').verbose_name
        self.assertEqual(field_label, 'description')


    def test_room_description_label(self):
        room = Room.objects.get(id=1)
        field_label = room._meta.get_field('slug').verbose_name
        self.assertEqual(field_label, 'slug')


    def test_room_participants_label(self):
        room = Room.objects.get(id=1)
        field_label = room._meta.get_field('participants').verbose_name
        self.assertEqual(field_label, 'participants')




    def test_room_name_max_length(self):
        room = Room.objects.get(id=1)
        max_length = room._meta.get_field('name').max_length
        self.assertEqual(max_length, 30)


    def test_room_description_max_length(self):
        room = Room.objects.get(id=1)
        max_length = room._meta.get_field('description').max_length
        self.assertEqual(max_length, 100)


    def test_room_slug_max_length(self):
        room = Room.objects.get(id=1)
        max_length = room._meta.get_field('slug').max_length
        self.assertEqual(max_length, 50)



    def test_room_name_is_name(self):
        room = Room.objects.get(id=1)
        expected_object_name = f'{room.name}'
        self.assertEqual(str(room), expected_object_name)
    






