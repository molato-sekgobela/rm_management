
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect, get_object_or_404
from django.core.mail import send_mail
from django.contrib.auth import login, logout
from django.urls import reverse
from django.contrib import messages
from django.http import HttpResponse
from .models import Client, DocumentRequest, UploadedDocument
from .forms import DocumentRequestForm, UploadDocumentForm, ClientForm
from django.core.signing import Signer, BadSignature
from django.views.generic import TemplateView, ListView, DeleteView, DetailView
from django.views.generic.edit import FormView
from django.views import View
from django.urls import reverse_lazy


# -------------------------------------
# Authentication related views
# -------------------------------------

class LoginView(FormView):
    template_name = 'login.html'
    form_class = AuthenticationForm

    def form_valid(self, form):
        """Authenticate and log user in; redirect superusers to dashboard."""
        user = form.get_user()
        if user.is_superuser:
            login(self.request, user)
            return redirect('dashboard')
        else:
            form.add_error(None, "You don't have access to the dashboard")
            return self.form_invalid(form)


class LogoutView(View):
    def get(self, request):
        """Logout the user and redirect them to login page."""
        logout(request)
        return redirect('login')


# -------------------------------------
# Dashboard and main views
# -------------------------------------

class DashboardView(TemplateView):
    template_name = 'dashboard.html'

    def get_context_data(self, **kwargs):
        """Add list of clients to the context."""
        context = super().get_context_data(**kwargs)
        context['clients'] = Client.objects.filter(rm=self.request.user)
        return context

    def dispatch(self, request, *args, **kwargs):
        """Ensure user is authenticated before accessing dashboard."""
        if not request.user.is_authenticated:
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)


# -------------------------------------
# Document Request related views
# -------------------------------------

class CreateRequestView(FormView):
    template_name = 'create_request.html'
    form_class = DocumentRequestForm
    success_url = reverse_lazy('dashboard')

    def dispatch(self, request, *args, **kwargs):
        """Validate client's email before creating a document request."""
        self.client = get_object_or_404(Client, id=kwargs['client_id'])
        if not self.client.is_email_verified:
            error_message = "Client's email not verified. Cannot create a document request."
            return redirect(reverse('error_view') + f'?error_message={error_message}')
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        """Pre-fill the form with client details."""
        kwargs = super().get_form_kwargs()
        kwargs['initial']['client'] = self.client
        return kwargs

    def form_valid(self, form):
        """On form validation, save the document request and email the client."""
        doc_request = form.save(commit=False)
        doc_request.save()

        upload_link = self.request.build_absolute_uri(reverse('upload_document', args=[doc_request.request_uuid]))
        send_mail(
            'Document Upload Request',
            f'Please click here {upload_link} for instructions on document upload',
            'from_email@example.com',
            [self.client.email],
            fail_silently=False,
        )

        return super().form_valid(form)


class UploadDocumentView(FormView):
    template_name = 'upload.html'
    form_class = UploadDocumentForm
    success_url = reverse_lazy('upload_success')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["uuid"] = self.kwargs['uuid']
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["num_files"] = 3  # Assuming 3 files by default
        return kwargs

    def form_valid(self, form):
        """On form validation, save uploaded documents and notify RM."""
        doc_request = get_object_or_404(DocumentRequest, request_uuid=self.kwargs['uuid'])
        for i in range(1, 4):  # Assuming 3 files
            field_name = f'file_{i}'
            uploaded_file = form.cleaned_data.get(field_name)
            if uploaded_file:
                UploadedDocument.objects.create(document_request=doc_request, document=uploaded_file)

        doc_request.is_completed = True
        doc_request.link_used = True
        doc_request.save()

        rm_email = doc_request.client.rm.email
        send_mail(
            'Document Successfully Uploaded',
            f'A document for {doc_request.client.name} was successfully uploaded.',
            'from_email@example.com',
            [rm_email],
            fail_silently=False,
        )

        return super().form_valid(form)

class DeleteDocumentRequestView(DeleteView):
    model = DocumentRequest
    template_name = 'confirm_delete.html'
    context_object_name = 'object'
    success_url = reverse_lazy('dashboard')

    def get_queryset(self):
        """Filter document requests based on the relationship manager."""
        return DocumentRequest.objects.filter(client__rm=self.request.user)

    def delete(self, request, *args, **kwargs):
        """On successful deletion, notify the user."""
        messages.success(request, 'Document request deleted successfully!')
        return super().delete(request, *args, **kwargs)


# -------------------------------------
# Client related views
# -------------------------------------

class AddClientView(FormView):
    template_name = 'add_client.html'
    form_class = ClientForm
    success_url = reverse_lazy('dashboard')

    def get_form_kwargs(self):
        """Pre-fill the form with relationship manager details."""
        kwargs = super().get_form_kwargs()
        kwargs['initial']['rm'] = self.request.user
        return kwargs

    def form_valid(self, form):
        """On form validation, save the client and send verification email."""
        client = form.save()  # Save the client object and get the instance

        # Generate a signed token for the client
        signer = Signer()
        signed_value = signer.sign(str(client.id))

        # Generate the verification URL
        verification_url = self.request.build_absolute_uri(reverse('verify_email', args=[signed_value]))

        # Send verification email
        send_mail(
            'Verify Your Email',
            f'Click the link to verify your email: {verification_url}',
            'from_email@example.com',
            [client.email],
            fail_silently=False,
        )

        return super().form_valid(form)


class ClientDocumentRequestsView(ListView):
    template_name = 'client_document_requests.html'
    context_object_name = 'document_requests'

    def get_queryset(self):
        """Fetch document requests for a specific client."""
        self.client = get_object_or_404(Client, pk=self.kwargs['client_id'])
        return DocumentRequest.objects.filter(client=self.client)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['client'] = self.client
        return context


class UploadedDocumentsView(DetailView):
    model = DocumentRequest
    template_name = 'view_uploaded_documents.html'
    context_object_name = 'doc_request'
    slug_field = 'request_uuid'
    slug_url_kwarg = 'uuid'
    success_url = reverse_lazy('upload_success')

    def get_context_data(self, **kwargs):
        """Fetch uploaded documents for a specific request."""
        context = super().get_context_data(**kwargs)
        context['uploaded_docs'] = UploadedDocument.objects.filter(document_request=self.object)
        return context


class VerifyEmail(View):
    def get(self, request, signed_value):
        """Verify client's email based on the signed token."""
        signer = Signer()
        try:
            client_id = signer.unsign(signed_value)
            client = Client.objects.get(id=client_id)
            client.is_email_verified = True
            client.save()
            return HttpResponse("Email successfully verified!")
        except BadSignature:
            return HttpResponse("Invalid or expired verification link.")
        except Client.DoesNotExist:
            return HttpResponse("Client does not exist.")


# -------------------------------------
# Miscellaneous views
# -------------------------------------

class ErrorView(TemplateView):
    template_name = 'error.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['error_message'] = self.request.GET.get('error_message', '')
        return context


class UploadSuccessView(TemplateView):
    template_name = 'upload_success.html'
