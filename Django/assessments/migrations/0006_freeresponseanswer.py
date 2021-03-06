# Generated by Django 4.0.1 on 2022-04-20 14:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('assessments', '0005_peerassessment_course_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='FreeResponseAnswer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('response_answer', models.CharField(max_length=256)),
                ('submission', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='assessments.submission')),
            ],
        ),
    ]
