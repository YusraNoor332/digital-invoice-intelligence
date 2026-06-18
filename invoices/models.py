import uuid
import random
from decimal import Decimal
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class TechnicianProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='technician_profile')
    employee_id = models.CharField(max_length=50, unique=True)
    phone_number = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.employee_id})"

class ProductInventory(models.Model):
    category = models.CharField(max_length=100)
    model_number = models.CharField(max_length=100)
    part_name = models.CharField(max_length=200)
    part_code = models.CharField(max_length=100, unique=True)
    price_pkr = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name_plural = "Product Inventories"

    def __str__(self):
        return f"{self.part_name} ({self.part_code})"

class ServiceType(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    worker_fee_pkr = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.name} (Rs. {self.worker_fee_pkr})"

def generate_otp():
    return str(random.randint(1000, 9999))

class Invoice(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    technician = models.ForeignKey(TechnicianProfile, on_delete=models.SET_NULL, null=True, related_name='invoices')
    
    # Customer Logs
    customer_name = models.CharField(max_length=200)
    customer_phone = models.CharField(max_length=20)
    customer_address = models.TextField()
    
    # Service/parts charges
    discount_pkr = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    # OTP Authentication
    otp_code = models.CharField(max_length=6, default=generate_otp)
    otp_verified = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def labor_charges_total(self):
        return sum(service.worker_fee_at_time_pkr for service in self.services.all())

    @property
    def total_before_tax(self):
        parts_total = sum(item.subtotal for item in self.items.all())
        return parts_total + self.labor_charges_total - self.discount_pkr

    @property
    def tax_amount(self):
        # 13% default tax calculation
        return round(self.total_before_tax * Decimal('0.13'), 2)

    @property
    def grand_total(self):
        return self.total_before_tax + self.tax_amount

    def __str__(self):
        return f"Invoice {self.id} - {self.customer_name}"

class InvoiceService(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='services')
    service = models.ForeignKey(ServiceType, on_delete=models.PROTECT)
    worker_fee_at_time_pkr = models.DecimalField(max_digits=10, decimal_places=2)

class InvoiceItem(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='items')
    part = models.ForeignKey(ProductInventory, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=1)
    price_at_time_pkr = models.DecimalField(max_digits=10, decimal_places=2)

    @property
    def subtotal(self):
        return self.quantity * self.price_at_time_pkr

class CustomerFeedback(models.Model):
    invoice = models.OneToOneField(Invoice, on_delete=models.CASCADE, related_name='feedback')
    
    verified_technician_name = models.CharField(max_length=200, help_text="Customer confirms the name of the technician", default="")
    
    # 5-point Likert choices for technician behavior, punctuality, and quality
    behavior_rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    resolution_quality = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    punctuality_rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    
    customer_remarks = models.TextField(blank=True, null=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback for Invoice {self.invoice.id}"
