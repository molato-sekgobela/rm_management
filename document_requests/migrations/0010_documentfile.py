# Generated by Django 4.2.5 on 2023-09-11 07:18

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('document_requests', '0009_alter_documentrequest_request_uuid'),
    ]

    operations = [
        migrations.CreateModel(
            name='DocumentFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='documents/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['pdf'])])),
                ('uploaded_document', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='files', to='document_requests.uploadeddocument')),
            ],
        ),
    ]