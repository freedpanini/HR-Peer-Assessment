# Generated by Django 4.0.1 on 2022-04-05 17:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0002_course_professor'),
    ]

    operations = [
        migrations.AddField(
            model_name='invitation',
            name='course_name',
            field=models.CharField(default='Test course', max_length=120),
            preserve_default=False,
        ),
    ]