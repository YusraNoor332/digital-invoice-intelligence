from django.urls import path
from . import views

urlpatterns = [
    # Auth
    path('technician/register/', views.register_view, name='register_view'),
    path('technician/login/', views.login_view, name='login_view'),
    path('technician/logout/', views.logout_view, name='logout_view'),

    # Custom Admin Dashboard
    path('admin/dashboard/', views.custom_admin_dashboard, name='custom_admin_dashboard'),
    path('admin/invoices/list/', views.admin_invoice_list, name='custom_admin_invoice_list'),
    path('admin/feedbacks/list/', views.admin_feedback_list, name='custom_admin_feedback_list'),
    path('admin/inventories/list/', views.admin_inventory_list, name='custom_admin_inventory_list'),
    path('admin/services/list/', views.admin_service_list, name='custom_admin_service_list'),
    path('admin/technicians/list/', views.admin_technician_list, name='custom_admin_technician_list'),
    
    # Global Search
    path('search/', views.global_search_view, name='global_search_view'),

    # Admin Uploads
    path('admin/upload/inventory/', views.admin_upload_inventory_excel, name='admin_upload_inventory_excel'),
    path('admin/upload/inventory/default/', views.admin_upload_inventory_excel, name='admin_upload'),
    path('admin/upload/services/', views.admin_upload_services_excel, name='admin_upload_services_excel'),

    # Technician / Invoice
    path('technician/dashboard/', views.technician_dashboard, name='technician_dashboard'),
    path('technician/create/', views.technician_invoice_create, name='technician_invoice_create'),
    path('load-parts/', views.load_parts, name='load_parts'),
    path('invoice/<uuid:pk>/', views.invoice_detail_view, name='invoice_detail_view'),
    path('invoice/<uuid:pk>/verify/', views.verify_otp_view, name='verify_otp_view'),
    path('invoice/<uuid:pk>/feedback/', views.submit_feedback_view, name='submit_feedback_view'),
]
