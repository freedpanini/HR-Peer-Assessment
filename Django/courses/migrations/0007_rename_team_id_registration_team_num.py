# Generated by Django 4.0.1 on 2022-04-12 19:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0006_team_course_id_team_team_num'),
    ]

    operations = [
        migrations.RenameField(
            model_name='registration',
            old_name='team_id',
            new_name='team_num',
        ),
    ]
