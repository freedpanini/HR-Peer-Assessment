# Generated by Django 4.0.1 on 2022-04-14 20:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0009_student_remove_team_student_list'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Student',
        ),
    ]
