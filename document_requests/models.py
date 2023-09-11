from django.db import models
import uuid
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator

# Relationship Manager Model
class RM(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Linking RM to a User instance
    name = models.CharField(max_length=100)  # Name of the Relationship Manager

    def __str__(self):
        return self.name

# Client Model
class Client(models.Model):
    name = models.CharField(max_length=100)  # Name of the Client
    email = models.EmailField()  # Client's email address
    rm = models.ForeignKey(User, on_delete=models.CASCADE)  # Relationship Manager assigned to the client
    is_email_verified = models.BooleanField(default=False)  # Email verification flag

    def __str__(self):
        return self.name

# Document Request Model
class DocumentRequest(models.Model):
    request_uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)  # Unique ID for the request
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date Created")  # Request creation date

    client = models.ForeignKey(Client, on_delete=models.CASCADE)  # Client related to the request
    is_completed = models.BooleanField(default=False)  # Flag to check if request is completed
    link_used = models.BooleanField(default=False)  # Flag to check if link was used

    def __str__(self):
        return f"Request {self.request_uuid} for {self.client.name}"

# Uploaded Document Model
class UploadedDocument(models.Model):
    document_request = models.ForeignKey(DocumentRequest, on_delete=models.CASCADE)  # The request related to the uploaded document
    document = models.FileField(upload_to='documents/')  # File field to store uploaded document

    def __str__(self):
        return f"Document for {self.document_request.client.name}"
