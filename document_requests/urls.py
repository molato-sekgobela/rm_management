from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

# Importing views
from .views import (
    DashboardView, CreateRequestView, UploadDocumentView, 
    AddClientView, ClientDocumentRequestsView, DeleteDocumentRequestView, 
    LoginView, LogoutView, UploadSuccessView, VerifyEmail, UploadedDocumentsView
)

# Define URL patterns
urlpatterns = [
    # Authentication views
    path('login/', LoginView.as_view(), name='login'),
    path('', LoginView.as_view(), name='login'),  # Default login route
    path('logout/', LogoutView.as_view(), name='logout_view'),
    
    # Dashboard view
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    
    # Client related views
    path('add_client/', AddClientView.as_view(), name='add_client'),
    path('client/<int:client_id>/requests/', ClientDocumentRequestsView.as_view(), name='client_document_requests'),
    
    # Document request views
    path('create_request/<int:client_id>/', CreateRequestView.as_view(), name='create_request'),
    path('upload/<uuid:uuid>/', UploadDocumentView.as_view(), name='upload_document'),
    path('document_request/delete/<int:pk>/', DeleteDocumentRequestView.as_view(), name='delete_document_request'),
    path('view_uploaded_documents/<uuid:uuid>/', UploadedDocumentsView.as_view(), name='view_uploaded_documents'),
    path('upload_success/', UploadSuccessView.as_view(), name='upload_success'),
    
    # Email verification
    path('verify_email/<str:signed_value>/', VerifyEmail.as_view(), name='verify_email'),
    
    # Error view
    path('error/', views.ErrorView.as_view(), name='error_view'),
]

# Add media URLs in DEBUG mode for local development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
