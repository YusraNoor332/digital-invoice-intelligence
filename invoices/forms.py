from django import forms
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from .models import Invoice, CustomerFeedback, ProductInventory, ServiceType, TechnicianProfile

class ExcelUploadForm(forms.Form):
    excel_file = forms.FileField(widget=forms.FileInput(attrs={'class': 'form-control', 'accept': '.xlsx'}))

class TechnicianRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))
    employee_id = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Emp ID (e.g., TECH-101)'}))
    phone_number = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
        }

class TechnicianLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))

class TechnicianInvoiceForm(forms.ModelForm):
    appliance = forms.ChoiceField(choices=[], required=True, label="Select Appliance", widget=forms.Select(attrs={
        'class': 'form-select',
        'hx-get': reverse_lazy('load_parts'),
        'hx-target': '#id_parts',
        'hx-trigger': 'change'
    }))
    
    parts = forms.ModelMultipleChoiceField(queryset=ProductInventory.objects.none(), required=False, widget=forms.SelectMultiple(attrs={
        'class': 'form-select',
        'id': 'id_parts'
    }))

    services = forms.ModelMultipleChoiceField(
        queryset=ServiceType.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'})
    )

    class Meta:
        model = Invoice
        fields = ['customer_name', 'customer_phone', 'customer_address', 'discount_pkr']
        widgets = {
            'customer_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Name'}),
            'customer_phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 03001234567'}),
            'customer_address': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Full Address'}),
            'discount_pkr': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        categories = ProductInventory.objects.values_list('category', flat=True).distinct()
        self.fields['appliance'].choices = [('', '--- Select Appliance ---')] + [(c, c) for c in categories]

        if 'appliance' in self.data:
            try:
                category = self.data.get('appliance')
                self.fields['parts'].queryset = ProductInventory.objects.filter(category=category)
            except (ValueError, TypeError):
                pass

class OTPVerificationForm(forms.Form):
    otp = forms.CharField(max_length=6, widget=forms.TextInput(attrs={'class': 'form-control text-center fs-4 letter-spacing-2', 'placeholder': 'Enter OTP', 'autocomplete': 'off'}))

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = CustomerFeedback
        fields = ['verified_technician_name', 'behavior_rating', 'resolution_quality', 'punctuality_rating', 'customer_remarks']
        CHOICES = [(i, str(i)) for i in range(5, 0, -1)]
        widgets = {
            'verified_technician_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Who serviced your appliance?'}),
            'behavior_rating': forms.RadioSelect(choices=CHOICES),
            'resolution_quality': forms.RadioSelect(choices=CHOICES),
            'punctuality_rating': forms.RadioSelect(choices=CHOICES),
            'customer_remarks': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Any additional comments...'}),
        }

