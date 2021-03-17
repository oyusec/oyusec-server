# Generated by Django 3.1.7 on 2021-03-17 09:04

import apps.core.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('competition', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Challenge',
            fields=[
                ('uuid', apps.core.models.UUIDField(blank=True, editable=False, max_length=32, primary_key=True, serialize=False, unique=True)),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='Created date')),
                ('last_updated_date', models.DateTimeField(auto_now=True, verbose_name='Last updated date')),
                ('name', models.CharField(max_length=30, unique=True, verbose_name='Name')),
                ('description', models.TextField(verbose_name='Description')),
                ('value', models.PositiveIntegerField(default=1000, null=True, verbose_name='Value')),
                ('category', models.CharField(max_length=100, null=True, verbose_name='Category')),
                ('state', models.CharField(choices=[('visible', 'visible'), ('hidden', 'hidden'), ('locked', 'locked')], default='visible', max_length=100, verbose_name='State')),
                ('max_attempts', models.PositiveIntegerField(default=0, verbose_name='Max attempts')),
                ('competition', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='competition.competition')),
            ],
            options={
                'verbose_name': 'Challenge',
            },
        ),
        migrations.CreateModel(
            name='Config',
            fields=[
                ('uuid', apps.core.models.UUIDField(blank=True, editable=False, max_length=32, primary_key=True, serialize=False, unique=True)),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='Created date')),
                ('last_updated_date', models.DateTimeField(auto_now=True, verbose_name='Last updated date')),
                ('key', models.CharField(db_index=True, max_length=200)),
                ('value', models.CharField(db_index=True, max_length=200)),
            ],
            options={
                'verbose_name': 'Config',
            },
        ),
        migrations.CreateModel(
            name='Submission',
            fields=[
                ('uuid', apps.core.models.UUIDField(blank=True, editable=False, max_length=32, primary_key=True, serialize=False, unique=True)),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='Created date')),
                ('last_updated_date', models.DateTimeField(auto_now=True, verbose_name='Last updated date')),
                ('submission', models.TextField(verbose_name='Submission')),
                ('challenge', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ctf.challenge', verbose_name='Challenge')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'verbose_name': 'Submission',
            },
        ),
        migrations.CreateModel(
            name='DynamicChallenge',
            fields=[
                ('challenge_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='ctf.challenge')),
                ('initial', models.PositiveIntegerField(default=1000, null=True, verbose_name='Initial value')),
                ('minimum', models.PositiveIntegerField(default=100, null=True, verbose_name='Minimum value')),
                ('decay', models.PositiveIntegerField(default=25, null=True, verbose_name='Decay')),
            ],
            options={
                'verbose_name': 'DynamicChallenge',
            },
            bases=('ctf.challenge',),
        ),
        migrations.CreateModel(
            name='Solve',
            fields=[
                ('submission_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='ctf.submission')),
            ],
            options={
                'verbose_name': 'Solve',
            },
            bases=('ctf.submission',),
        ),
        migrations.CreateModel(
            name='StandardChallenge',
            fields=[
                ('challenge_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='ctf.challenge')),
            ],
            options={
                'verbose_name': 'StandardChallenge',
            },
            bases=('ctf.challenge',),
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('uuid', apps.core.models.UUIDField(blank=True, editable=False, max_length=32, primary_key=True, serialize=False, unique=True)),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='Created date')),
                ('last_updated_date', models.DateTimeField(auto_now=True, verbose_name='Last updated date')),
                ('content', models.CharField(max_length=80)),
                ('challenge', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ctf.challenge')),
            ],
            options={
                'verbose_name': 'Tag',
            },
        ),
        migrations.CreateModel(
            name='Hint',
            fields=[
                ('uuid', apps.core.models.UUIDField(blank=True, editable=False, max_length=32, primary_key=True, serialize=False, unique=True)),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='Created date')),
                ('last_updated_date', models.DateTimeField(auto_now=True, verbose_name='Last updated date')),
                ('content', models.CharField(max_length=100, verbose_name='Зөвлөгөө')),
                ('state', models.CharField(choices=[('visible', 'visible'), ('hidden', 'hidden'), ('locked', 'locked')], default='visible', max_length=100, verbose_name='State')),
                ('cost', models.PositiveIntegerField(default=0, verbose_name='Cost')),
                ('challenge', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ctf.challenge', verbose_name='Challenge')),
            ],
            options={
                'verbose_name': 'Hint',
            },
        ),
        migrations.CreateModel(
            name='Flag',
            fields=[
                ('uuid', apps.core.models.UUIDField(blank=True, editable=False, max_length=32, primary_key=True, serialize=False, unique=True)),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='Created date')),
                ('last_updated_date', models.DateTimeField(auto_now=True, verbose_name='Last updated date')),
                ('content', models.CharField(max_length=100, verbose_name='Content')),
                ('challenge', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ctf.challenge')),
            ],
            options={
                'verbose_name': 'Flag',
            },
        ),
        migrations.AddField(
            model_name='challenge',
            name='flags',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='challenge_flag', to='ctf.flag', verbose_name='Flag'),
        ),
        migrations.AddField(
            model_name='challenge',
            name='hints',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='challenge_hint', to='ctf.hint'),
        ),
        migrations.AddField(
            model_name='challenge',
            name='tags',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='challenge_tag', to='ctf.tag'),
        ),
    ]
