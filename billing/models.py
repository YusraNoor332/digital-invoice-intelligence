import uuid
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class TechnicianProfile(models.Model):
    """
    Linked to Django User to extend with technician-specific details.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='technician_profile')
    phone_number = models.CharField(max_length=20, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Technician: {self.user.get_full_name() or self.user.username}"

class ProductInventory(models.Model):
    """
    Master inventory for parts imported from Excel.
    """
    category = models.CharField(max_length=100)
    model_number = models.CharField(max_length=100)
    part_name = models.CharField(max_length=200)
    part_code = models.CharField(max_length=100, unique=True)
    price_pkr = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name_plural = "Product Inventories"

    def __str__(self):
        return f"{self.part_name} ({self.part_code}) - Rs.{self.price_pkr}"

class Invoice(models.Model):
    """
    Secure Invoice using UUID.
    """
    STATUS_CHOICES = [
        ('DRAFT', 'Draft'),
        ('ISSUED', 'Issued'),
        ('PAID', 'Paid'),
        ('CANCELLED', 'Cancelled'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    technician = models.ForeignKey(TechnicianProfile, on_delete=models.SET_NULL, null=True, related_name='invoices')
    
    # Customer Details
    customer_name = models.CharField(max_length=200)
    customer_phone = models.CharField(max_length=20)
    customer_address = models.TextField()
    
    # Financial Details
    labor_charges_pkr = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    discount_pkr = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    # Tracking
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='DRAFT')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def total_before_tax(self):
        return sum(item.subtotal for item in self.items.all()) + self.labor_charges_pkr - self.discount_pkr

    @property
    def tax_amount(self):
        # 13% Sales Tax
        from decimal import Decimal
        return round(self.total_before_tax * Decimal('0.13'), 2)

    @property
    def grand_total(self):
        return self.total_before_tax + self.tax_amount

    def __str__(self):
        return f"Invoice {self.id} - {self.customer_name}"

class InvoiceItem(models.Model):
    """
    Line items for the Invoice.
    """
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='items')
    part = models.ForeignKey(ProductInventory, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=1)
    price_at_time_pkr = models.DecimalField(max_digits=10, decimal_places=2, help_text="Price of part when invoice was created")

    @property
    def subtotal(self):
        return self.quantity * self.price_at_time_pkr

    def __str__(self):
        return f"{self.quantity}x {self.part.part_code} for Invoice {self.invoice.id}"

class CustomerFeedback(models.Model):
    """
    1:1 linked to Invoice to capture Likert scale survey responses.
    """
    invoice = models.OneToOneField(Invoice, on_delete=models.CASCADE, related_name='feedback')
    
    # 5-point Likert scale (1=Strongly Disagree, 5=Strongly Agree)
    professionalism = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], help_text="The technician conducted themselves professionally and politely.")
    issue_resolved = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], help_text="The machine breakdown or product fault was effectively resolved.")
    punctuality = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], help_text="The technician arrived precisely within the committed time window.")
    
    remarks = models.TextField(blank=True, null=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback for Invoice {self.invoice.id}"
