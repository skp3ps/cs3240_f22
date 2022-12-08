from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class BaseModel(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    class Meta:
        abstract = True

# code to attach a profile to user one-to-one modified from https://simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html#onetoone
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Course(BaseModel):
    subject = models.CharField(max_length=4)
    semester_code = models.IntegerField()
    course_number = models.IntegerField()
    course_section = models.CharField(max_length=4)
    catalog_number = models.CharField(max_length=6)
    instructor_name = models.CharField(max_length=50)
    instructor_email = models.CharField(max_length=50)
    description = models.CharField(max_length=500)
    units = models.CharField(max_length=10)
    component = models.CharField(max_length=4)
    class_capacity = models.IntegerField()
    wait_list = models.IntegerField()
    wait_cap = models.IntegerField()
    enrollment_total = models.IntegerField()
    enrollment_available = models.IntegerField()
    meetings_days = models.CharField(max_length=14)
    meetings_start_time = models.CharField(max_length=50)
    meetings_end_time = models.CharField(max_length=50)
    facility_description = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.subject + ' ' + str(self.catalog_number) + '.' + self.course_section

CONDITION_CHOICES=(('NEW','new'),('EXCELLENT','excellent'),('GOOD','good'),('FAIR','fair'),('POOR','poor'))
class Book(BaseModel):
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    isbn = models.CharField(max_length=15)
    year = models.PositiveIntegerField(default=0000)
    price = models.FloatField(default=0)
    version = models.PositiveIntegerField(default=0)
    condition = models.CharField(max_length=9, choices=CONDITION_CHOICES, default='GOOD')
    image = models.ImageField(default='images/defaultCover.png', upload_to='images/')
    favorited_by = models.ManyToManyField(User, related_name="favorited")

    def __str__(self) -> str:
        return self.title
