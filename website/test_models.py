from django.db import models
from django.test import TestCase
from .models import Course, Book
from django.contrib.auth.models import User



# Create your tests here.
class BookModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        course = Course.objects.create(subject='CS', semester_code=1228, course_number=15991, course_section='001', catalog_number='3240', instructor_name='Paul McBurney',instructor_email='pm8fc@virginia.edu', description='Computer Science', 
        units='cs class units', component='abcd', class_capacity=100, wait_list=140, wait_cap=50, enrollment_total=500, enrollment_available=500, meetings_days='TF',
        meetings_start_time='2022-01-01', meetings_end_time='2022-12-31', facility_description='good facility')
        # user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
        user = User.objects.create()
        Book.objects.create(seller=user, course=course, title='Comp Sci', isbn='1234', year=2002, price=100.0, version=1, condition='good')
        print("list of courses in DB: " + str(Course.objects.count()))
        print("list of books in DB: " + str(Book.objects.count()))


    def test_course_semester_code_label(self):
        course = Course.objects.get(id=1)
        field_label = course._meta.get_field('semester_code').verbose_name
        self.assertEqual(field_label, 'semester code')


    def test_course_course_number_label(self):
        course = Course.objects.get(id=1)
        field_label = course._meta.get_field('course_number').verbose_name
        self.assertEqual(field_label, 'course number')



    def test_course_course_section_label(self):
        course = Course.objects.get(id=1)
        field_label = course._meta.get_field('course_section').verbose_name
        self.assertEqual(field_label, 'course section')



    def test_course_catalog_number_label(self):
        course = Course.objects.get(id=1)
        field_label = course._meta.get_field('catalog_number').verbose_name
        self.assertEqual(field_label, 'catalog number')


    def test_course_instructor_name_label(self):
        course = Course.objects.get(id=1)
        field_label = course._meta.get_field('instructor_name').verbose_name
        self.assertEqual(field_label, 'instructor name')


    def test_course_instructor_email_label(self):
        course = Course.objects.get(id=1)
        field_label = course._meta.get_field('instructor_email').verbose_name
        self.assertEqual(field_label, 'instructor email')


    def test_course_course_section_max_length(self):
        course = Course.objects.get(id=1)
        max_length = course._meta.get_field('course_section').max_length
        self.assertEqual(max_length, 4)


    def test_course_catalog_number_max_length(self):
        course = Course.objects.get(id=1)
        max_length = course._meta.get_field('catalog_number').max_length
        self.assertEqual(max_length, 6)


    def test_course_instructor_name_max_length(self):
        course = Course.objects.get(id=1)
        max_length = course._meta.get_field('instructor_name').max_length
        self.assertEqual(max_length, 50)


    def test_course_instructor_email_max_length(self):
        course = Course.objects.get(id=1)
        max_length = course._meta.get_field('instructor_email').max_length
        self.assertEqual(max_length, 50)


    

    def test_book_seller_label(self):
        book = Book.objects.get(id=1)
        field_label = book._meta.get_field('seller').verbose_name
        self.assertEqual(field_label, 'seller')


    def test_book_course_label(self):
        book = Book.objects.get(id=1)
        field_label = book._meta.get_field('course').verbose_name
        self.assertEqual(field_label, 'course')



    def test_book_title_label(self):
        book = Book.objects.get(id=1)
        field_label = book._meta.get_field('title').verbose_name
        self.assertEqual(field_label, 'title')



    def test_book_isbn_label(self):
        book = Book.objects.get(id=1)
        field_label = book._meta.get_field('isbn').verbose_name
        self.assertEqual(field_label, 'isbn')


    def test_book_year_label(self):
        book = Book.objects.get(id=1)
        field_label = book._meta.get_field('year').verbose_name
        self.assertEqual(field_label, 'year')


    def test_book_price_label(self):
        book = Book.objects.get(id=1)
        field_label = book._meta.get_field('price').verbose_name
        self.assertEqual(field_label, 'price')


    def test_book_version_label(self):
        book = Book.objects.get(id=1)
        field_label = book._meta.get_field('version').verbose_name
        self.assertEqual(field_label, 'version')

    def test_book_condition_label(self):
        book = Book.objects.get(id=1)
        field_label = book._meta.get_field('condition').verbose_name
        self.assertEqual(field_label, 'condition')


    def test_book_image_label(self):
        book = Book.objects.get(id=1)
        field_label = book._meta.get_field('image').verbose_name
        self.assertEqual(field_label, 'image')



    def test_book_title_max_length(self):
        book = Book.objects.get(id=1)
        max_length = book._meta.get_field('title').max_length
        self.assertEqual(max_length, 100)


    def test_book_isbn_max_length(self):
        book = Book.objects.get(id=1)
        max_length = book._meta.get_field('isbn').max_length
        self.assertEqual(max_length, 15)


    def test_book_isbn_condition_length(self):
        book = Book.objects.get(id=1)
        max_length = book._meta.get_field('condition').max_length
        self.assertEqual(max_length, 9)

    def test_book_name_is_title(self):
        book = Book.objects.get(id=1)
        expected_object_name = f'{book.title}'
        self.assertEqual(str(book), expected_object_name)
    


    def test_course_name_is_subject_space_catalog_number_period_course_section(self):
        course = Course.objects.get(id=1)
        expected_object_name = f'{course.subject} {course.catalog_number}.{course.course_section}'
        self.assertEqual(str(course), expected_object_name)




