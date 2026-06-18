from django.contrib import admin
from .models import TechnicianProfile, ProductInventory, ServiceType, Invoice, InvoiceItem, InvoiceService, CustomerFeedback

@admin.register(TechnicianProfile)
class TechnicianProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'employee_id', 'phone_number')
    search_fields = ('user__username', 'employee_id')

@admin.register(ProductInventory)
class ProductInventoryAdmin(admin.ModelAdmin):
    list_display = ('part_code', 'part_name', 'model_number', 'price_pkr')
    search_fields = ('part_code', 'part_name')

@admin.register(ServiceType)
class ServiceTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'worker_fee_pkr')

class InvoiceItemInline(admin.TabularInline):
    model = InvoiceItem
    extra = 0

class InvoiceServiceInline(admin.TabularInline):
    model = InvoiceService
    extra = 0

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer_name', 'grand_total', 'created_at', 'otp_verified')
    inlines = [InvoiceItemInline, InvoiceServiceInline]

@admin.register(CustomerFeedback)
class CustomerFeedbackAdmin(admin.ModelAdmin):
    list_display = ('invoice', 'verified_technician_name', 'behavior_rating', 'resolution_quality', 'punctuality_rating')
