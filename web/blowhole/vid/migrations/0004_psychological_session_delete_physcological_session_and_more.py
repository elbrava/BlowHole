# Generated by Django 4.0 on 2022-05-04 17:18

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('vid', '0003_post_psychological_sessions_newuser_ratings'),
    ]

    operations = [
        migrations.CreateModel(
            name='Psychological_Session',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_start', models.DateTimeField(default=django.utils.timezone.now)),
                ('symptoms', models.CharField(max_length=1500)),
                ('diagnosis', models.CharField(max_length=150)),
                ('story', models.CharField(max_length=150)),
                ('feelings', models.CharField(max_length=150)),
                ('link', models.CharField(max_length=150)),
                ('psychologist', models.CharField(max_length=150)),
                ('counselee', models.CharField(max_length=150)),
                ('storage_id_sessions', models.CharField(max_length=150)),
                ('in_session', models.BooleanField(default=True)),
            ],
        ),
        migrations.DeleteModel(
            name='Physcological_session',
        ),
        migrations.DeleteModel(
            name='Psychological_Sessions',
        ),
    ]
