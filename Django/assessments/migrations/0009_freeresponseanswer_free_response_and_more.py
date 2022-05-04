# Generated by Django 4.0.1 on 2022-05-03 16:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('assessments', '0008_option_value'),
    ]

    operations = [
        migrations.AddField(
            model_name='freeresponseanswer',
            name='free_response',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='assessments.freeresponse'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='submission',
            name='submitted_by',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='creator', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='submission',
            name='assigned_to',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assigned', to=settings.AUTH_USER_MODEL),
        ),
    ]