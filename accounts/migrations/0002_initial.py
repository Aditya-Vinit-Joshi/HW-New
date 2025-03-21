# Generated by Django 5.1.6 on 2025-03-13 03:39

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
        ('auth', '0012_alter_user_first_name_max_length'),
        ('resources', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='interests',
            field=models.ManyToManyField(blank=True, to='resources.category'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='saved_resources',
            field=models.ManyToManyField(blank=True, to='resources.resource'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions'),
        ),
    ]
