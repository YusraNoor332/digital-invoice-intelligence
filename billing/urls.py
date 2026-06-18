from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_invoice, name='create_invoice'),
    path('load-parts/', views.load_parts, name='load_parts'),
    path('invoice/<uuid:invoice_id>/', views.invoice_detail, name='invoice_detail'),
    path('invoice/<uuid:invoice_id>/feedback/', views.submit_feedback, name='submit_feedback'),
]
