# Generated by Django 3.1.7 on 2021-03-25 12:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ctf', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='challenge',
            name='flags',
        ),
    ]