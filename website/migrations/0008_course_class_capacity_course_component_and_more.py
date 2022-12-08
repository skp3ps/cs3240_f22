# Generated by Django 4.1.1 on 2022-11-11 21:39

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0007_book_favorited_by'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='class_capacity',
            field=models.IntegerField(default=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='course',
            name='component',
            field=models.CharField(default='LEC', max_length=4),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='course',
            name='description',
            field=models.CharField(default='desc', max_length=500),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='course',
            name='enrollment_total',
            field=models.IntegerField(default=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='course',
            name='facility_description',
            field=models.CharField(default='fac desc', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='course',
            name='meetings_days',
            field=models.CharField(default='MoWeFr', max_length=14),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='course',
            name='meetings_end_time',
            field=models.DateTimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='course',
            name='meetings_start_time',
            field=models.DateTimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='course',
            name='units',
            field=models.CharField(default=3, max_length=2),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='course',
            name='wait_cap',
            field=models.IntegerField(default=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='course',
            name='wait_list',
            field=models.IntegerField(default=20),
            preserve_default=False,
        ),
    ]
