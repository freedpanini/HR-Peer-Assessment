# Generated by Django 4.0.1 on 2022-04-06 03:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0004_registration_course_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='invitation',
            old_name='course_name',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='registration',
            old_name='course_name',
            new_name='name',
        ),
    ]
