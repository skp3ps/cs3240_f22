# Generated by Django 4.1.1 on 2022-12-05 09:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0015_remove_profile_friends'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Friend_Request',
        ),
    ]
