from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Invoice, ProductInventory, InvoiceItem
from .forms import InvoiceCreationForm, CustomerFeedbackForm

def create_invoice(request):
    """
    Technician view to create a new invoice.
    """
    if request.method == 'POST':
        form = InvoiceCreationForm(request.POST)
        if form.is_valid():
            invoice = form.save(commit=False)
            if hasattr(request.user, 'technician_profile'):
                invoice.technician = request.user.technician_profile
            invoice.save()
            
            # Save related parts
            parts = form.cleaned_data.get('parts')
            for part in parts:
                InvoiceItem.objects.create(
                    invoice=invoice,
                    part=part,
                    quantity=1,
                    price_at_time_pkr=part.price_pkr
                )
            
            return redirect('invoice_detail', invoice_id=invoice.id)
    else:
        form = InvoiceCreationForm()
        
    return render(request, 'billing/invoice_form.html', {'form': form})

def load_parts(request):
    """
    HTMX endpoint: Returns parts for a selected appliance model as <option> elements.
    """
    model_number = request.GET.get('appliance_model')
    parts = ProductInventory.objects.filter(model_number=model_number).order_by('part_name')
    return render(request, 'billing/partials/parts_dropdown_list.html', {'parts': parts})

def invoice_detail(request, invoice_id):
    """
    Customer read-only invoice view with Likert feedback form.
    """
    invoice = get_object_or_404(Invoice, id=invoice_id)
    
    # If feedback already exists, don't show the form
    has_feedback = hasattr(invoice, 'feedback')
    form = CustomerFeedbackForm() if not has_feedback else None

    return render(request, 'billing/invoice_detail.html', {
        'invoice': invoice,
        'form': form,
        'has_feedback': has_feedback
    })

def submit_feedback(request, invoice_id):
    """
    HTMX endpoint: Submits the customer feedback and returns a success message.
    """
    invoice = get_object_or_404(Invoice, id=invoice_id)
    if request.method == 'POST':
        form = CustomerFeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.invoice = invoice
            feedback.save()
            return HttpResponse('<div class="alert alert-success fw-bold text-center">Thank You! Your verification and feedback have been recorded.</div>')
        return render(request, 'billing/partials/survey_form.html', {'form': form, 'invoice': invoice})
    return HttpResponse("Invalid request.", status=400)
