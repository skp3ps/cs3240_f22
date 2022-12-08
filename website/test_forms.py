from django.test import TestCase
from .models import Course, Book
from .forms import BookForm

# Create your tests here.
class BookFormTest(TestCase):
    def test_boook_form__fields_label(self):
        form = BookForm()
        self.assertTrue(form.fields['title'].label is None or form.fields['title'].label == 'Title')
        self.assertTrue(form.fields['isbn'].label is None or form.fields['isbn'].label == 'Isbn')
        self.assertTrue(form.fields['year'].label is None or form.fields['year'].label == 'Year')
        self.assertTrue(form.fields['price'].label is None or form.fields['price'].label == 'Price')
        self.assertTrue(form.fields['version'].label is None or form.fields['version'].label == 'Version')
        self.assertTrue(form.fields['condition'].label is None or form.fields['condition'].label == 'Condition')
        self.assertTrue(form.fields['image'].label is None or form.fields['image'].label == 'Image')                                        


    def test_boook_form_is_valid(self):
        form = BookForm(data={'title': 'Comp Sci', 'isbn': '1234', 'year': 2002, 'price': 100.0, 'version': 1, 'condition': 'GOOD', 'image': 'path/static/website/defaultCover.png'})        
        self.assertTrue(form.is_valid())

    def test_boook_form_is_invalid(self):
        form = BookForm(data={'title': 'Comp Sci', 'isbn': '1234123412341234', 'year': 2002, 'price': 100.0, 'version': 1, 'condition': 'GOOD', 'image': 'path/static/website/defaultCover.png'})        
        self.assertFalse(form.is_valid())

