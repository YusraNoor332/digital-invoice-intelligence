from django.contrib import admin
from .models import TechnicianProfile, ProductInventory, Invoice, InvoiceItem, CustomerFeedback

@admin.register(TechnicianProfile)
class TechnicianProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number', 'is_active')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'phone_number')

@admin.register(ProductInventory)
class ProductInventoryAdmin(admin.ModelAdmin):
    list_display = ('part_code', 'part_name', 'category', 'model_number', 'price_pkr')
    list_filter = ('category', 'model_number')
    search_fields = ('part_name', 'part_code', 'model_number')

class InvoiceItemInline(admin.TabularInline):
    model = InvoiceItem
    extra = 1

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer_name', 'technician', 'status', 'grand_total', 'created_at')
    list_filter = ('status', 'created_at', 'technician')
    search_fields = ('id', 'customer_name', 'customer_phone')
    inlines = [InvoiceItemInline]
    readonly_fields = ('id', 'created_at', 'updated_at')

@admin.register(CustomerFeedback)
class CustomerFeedbackAdmin(admin.ModelAdmin):
    list_display = ('invoice', 'technician_behavior', 'punctuality', 'service_quality', 'submitted_at')
    list_filter = ('technician_behavior', 'punctuality', 'service_quality', 'submitted_at')
    search_fields = ('invoice__id', 'invoice__customer_name')
