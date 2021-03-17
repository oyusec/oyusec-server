# Generated by Django 3.1.7 on 2021-03-17 03:03

import apps.core.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Competition',
            fields=[
                ('uuid', apps.core.models.UUIDField(blank=True, editable=False, max_length=32, primary_key=True, serialize=False, unique=True)),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='Created date')),
                ('last_updated_date', models.DateTimeField(auto_now=True, verbose_name='Last updated date')),
                ('name', models.CharField(max_length=100, verbose_name='Name')),
                ('description', models.TextField(verbose_name='Description')),
                ('status', models.CharField(choices=[('upcoming', 'upcoming'), ('archive', 'archive'), ('live', 'live')], default='upcoming', max_length=100, verbose_name='Status')),
                ('slug', models.SlugField(unique=True)),
                ('photo', models.URLField(blank=True, default='https://github.com/OyuTech/Utils/blob/main/oyusec/oyusec.png', null=True)),
                ('rule', models.TextField()),
                ('prize', models.TextField()),
            ],
            options={
                'verbose_name': 'Competition',
            },
        ),
        migrations.CreateModel(
            name='CompetitionUser',
            fields=[
                ('uuid', apps.core.models.UUIDField(blank=True, editable=False, max_length=32, primary_key=True, serialize=False, unique=True)),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='Created date')),
                ('last_updated_date', models.DateTimeField(auto_now=True, verbose_name='Last updated date')),
                ('score', models.PositiveIntegerField(default=0, verbose_name='Score')),
                ('competition', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='competition.competition')),
            ],
            options={
                'verbose_name': 'Competition User',
            },
        ),
    ]
