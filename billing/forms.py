from django import forms
from .models import Invoice, CustomerFeedback, ProductInventory

class InvoiceCreationForm(forms.ModelForm):
    appliance_model = forms.ChoiceField(choices=[], required=True, widget=forms.Select(attrs={
        'class': 'form-select',
        'hx-get': '/billing/load-parts/',
        'hx-target': '#id_parts',
        'hx-trigger': 'change'
    }))
    parts = forms.ModelMultipleChoiceField(queryset=ProductInventory.objects.none(), required=False, widget=forms.SelectMultiple(attrs={
        'class': 'form-select',
        'id': 'id_parts'
    }))

    class Meta:
        model = Invoice
        fields = ['customer_name', 'customer_phone', 'customer_address', 'labor_charges_pkr', 'discount_pkr']
        widgets = {
            'customer_name': forms.TextInput(attrs={'class': 'form-control'}),
            'customer_phone': forms.TextInput(attrs={'class': 'form-control'}),
            'customer_address': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'labor_charges_pkr': forms.NumberInput(attrs={'class': 'form-control'}),
            'discount_pkr': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Populate unique appliance models
        models = ProductInventory.objects.values_list('model_number', flat=True).distinct()
        self.fields['appliance_model'].choices = [('', '---------')] + [(m, m) for m in models]

        if 'appliance_model' in self.data:
            try:
                model_num = self.data.get('appliance_model')
                self.fields['parts'].queryset = ProductInventory.objects.filter(model_number=model_number).order_by('part_name')
            except (ValueError, TypeError):
                pass

class CustomerFeedbackForm(forms.ModelForm):
    class Meta:
        model = CustomerFeedback
        fields = ['professionalism', 'issue_resolved', 'punctuality', 'remarks']
        widgets = {
            'professionalism': forms.RadioSelect(choices=[(i, str(i)) for i in range(1, 6)]),
            'issue_resolved': forms.RadioSelect(choices=[(i, str(i)) for i in range(1, 6)]),
            'punctuality': forms.RadioSelect(choices=[(i, str(i)) for i in range(1, 6)]),
            'remarks': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
