# Generated by Django 3.2.8 on 2021-10-05 16:51

import api.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import gdstorage.storage


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Amenities',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
            ],
            options={
                'verbose_name': 'Amenity',
                'verbose_name_plural': 'Amenities',
            },
        ),
        migrations.CreateModel(
            name='Barbershop',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('address', models.CharField(max_length=255)),
                ('contact_number', models.CharField(blank=True, max_length=11, null=True)),
                ('photo', models.ImageField(blank=True, null=True, storage=gdstorage.storage.GoogleDriveStorage(), upload_to='banners', validators=[api.models.validate_file_extension])),
                ('rating', models.FloatField(default=0)),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
                ('verified', models.BooleanField(default=False)),
                ('amenities', models.ManyToManyField(related_name='amenities', to='api.Amenities')),
            ],
        ),
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('rating', models.FloatField()),
                ('type', models.CharField(max_length=8)),
            ],
            options={
                'verbose_name': 'Comment',
                'verbose_name_plural': 'Comments',
            },
        ),
        migrations.CreateModel(
            name='OperationHours',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.CharField(max_length=255)),
                ('opening_time', models.TimeField()),
                ('closing_time', models.TimeField()),
            ],
            options={
                'verbose_name': 'OperationHour',
                'verbose_name_plural': 'OperationHours',
            },
        ),
        migrations.CreateModel(
            name='Services',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('price', models.FloatField(default=0)),
            ],
            options={
                'verbose_name': 'Service',
                'verbose_name_plural': 'Services',
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contact_number', models.CharField(blank=True, max_length=11, null=True)),
                ('photo', models.ImageField(blank=True, null=True, storage=gdstorage.storage.GoogleDriveStorage(), upload_to='profiles', validators=[api.models.validate_file_extension])),
                ('address', models.CharField(blank=True, max_length=255, null=True)),
                ('account_type', models.CharField(max_length=5)),
                ('barbershop', models.ManyToManyField(related_name='shops', to='api.Barbershop')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='barbershop',
            name='comments',
            field=models.ManyToManyField(related_name='comments', to='api.Comments'),
        ),
        migrations.AddField(
            model_name='barbershop',
            name='favorites',
            field=models.ManyToManyField(related_name='favorites', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='barbershop',
            name='hours',
            field=models.ManyToManyField(related_name='hours', to='api.OperationHours'),
        ),
        migrations.AddField(
            model_name='barbershop',
            name='services',
            field=models.ManyToManyField(related_name='services', to='api.Services'),
        ),
    ]
