# Generated by Django 4.1.1 on 2022-10-16 22:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='condition',
            field=models.CharField(choices=[('NEW', 'new'), ('EXCELLENT', 'excellent'), ('GOOD', 'good'), ('FAIR', 'fair'), ('POOR', 'poor')], default='GOOD', max_length=9),
        ),
        migrations.AddField(
            model_name='book',
            name='image',
            field=models.ImageField(default='path/static/website/defaultCover.png', upload_to=''),
        ),
        migrations.AddField(
            model_name='book',
            name='price',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='book',
            name='version',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='book',
            name='year',
            field=models.IntegerField(default=0),
        ),
    ]
