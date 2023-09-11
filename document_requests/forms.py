from django import forms
from .models import DocumentRequest, UploadedDocument, Client
from django.core.validators import FileExtensionValidator

# Form for creating a new Document Request
class DocumentRequestForm(forms.ModelForm):
    
    class Meta:
        model = DocumentRequest
        fields = ['client']  # Only the client field is needed since other fields have default values

# Form for uploading documents by the client
class UploadDocumentForm(forms.Form):

    # The __init__ method dynamically generates file fields based on the num_files parameter
    def __init__(self, num_files=3, *args, **kwargs):  # Default number of file fields is 3
        super(UploadDocumentForm, self).__init__(*args, **kwargs)
        
        # Dynamically adding file fields to the form
        for i in range(num_files):
            field_name = f'file_{i+1}'  # e.g., file_1, file_2, ...
            
            # Adding a file field with a validator to ensure only PDFs are uploaded
            self.fields[field_name] = forms.FileField(
                validators=[FileExtensionValidator(allowed_extensions=['pdf'])],
                required=True
            )

# Form for adding a new client
class ClientForm(forms.ModelForm):
    
    class Meta:
        model = Client
        fields = ['name', 'email', 'rm']  # Including fields: name, email, and assigned relationship manager
