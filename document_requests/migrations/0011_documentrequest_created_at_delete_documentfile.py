# Generated by Django 4.2.5 on 2023-09-11 09:19

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('document_requests', '0010_documentfile'),
    ]

    operations = [
        migrations.AddField(
            model_name='documentrequest',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='Date Created'),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='DocumentFile',
        ),
    ]
