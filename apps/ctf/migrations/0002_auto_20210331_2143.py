# Generated by Django 3.1.7 on 2021-03-31 13:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ctf', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='challenge',
            name='solution',
            field=models.CharField(blank=True, default='', max_length=500, null=True, verbose_name='Solution'),
        ),
    ]
