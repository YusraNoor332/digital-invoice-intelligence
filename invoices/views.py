from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
import json
from django.db.models import Count, Q, Sum
from django.db.models.functions import TruncMonth
from django.http import JsonResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.admin.views.decorators import staff_member_required
from .models import Invoice, ProductInventory, InvoiceItem, InvoiceService, TechnicianProfile, ServiceType, CustomerFeedback
from .forms import TechnicianInvoiceForm, FeedbackForm, ExcelUploadForm, OTPVerificationForm, TechnicianRegistrationForm, TechnicianLoginForm
from .services import ingest_inventory_excel, ingest_services_excel

# Authentication Views
def register_view(request):
    if request.method == 'POST':
        form = TechnicianRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            TechnicianProfile.objects.create(
                user=user,
                employee_id=form.cleaned_data['employee_id'],
                phone_number=form.cleaned_data['phone_number']
            )
            login(request, user)
            return redirect('technician_dashboard')
    else:
        form = TechnicianRegistrationForm()
    return render(request, 'invoices/auth/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = TechnicianLoginForm(request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                return redirect('technician_dashboard')
            else:
                form.add_error(None, 'Invalid username or password')
    else:
        form = TechnicianLoginForm()
    return render(request, 'invoices/auth/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login_view')

# Custom Admin Upload Views
@staff_member_required
def admin_upload_inventory_excel(request):
    if request.method == 'POST':
        form = ExcelUploadForm(request.POST, request.FILES)
        if form.is_valid():
            result = ingest_inventory_excel(request.FILES['excel_file'])
            if result['success']:
                messages.success(request, f"Successfully processed {result['processed']} parts (Created: {result['created']}, Updated: {result['updated']}).")
                return redirect('admin:invoices_productinventory_changelist')
            messages.error(request, result['error'])
    else:
        form = ExcelUploadForm()
    return render(request, 'invoices/admin/upload.html', {'form': form, 'title': 'Upload Parts Inventory', 'opts': ProductInventory._meta})

@staff_member_required
def admin_upload_services_excel(request):
    if request.method == 'POST':
        form = ExcelUploadForm(request.POST, request.FILES)
        if form.is_valid():
            result = ingest_services_excel(request.FILES['excel_file'])
            if result['success']:
                messages.success(request, f"Successfully processed {result['processed']} services (Created: {result['created']}, Updated: {result['updated']}).")
                return redirect('admin:invoices_servicetype_changelist')
            messages.error(request, result['error'])
    else:
        form = ExcelUploadForm()
    return render(request, 'invoices/admin/upload.html', {'form': form, 'title': 'Upload Services List', 'opts': ServiceType._meta})

# Technician Views
@login_required(login_url='login_view')
def technician_dashboard(request):
    invoices = Invoice.objects.filter(technician=request.user.technician_profile).order_by('-created_at')
    total_invoices = invoices.count()
    recent_invoices = invoices[:5]
    
    return render(request, 'invoices/technician/dashboard.html', {
        'total_invoices': total_invoices,
        'recent_invoices': recent_invoices
    })

@login_required(login_url='login_view')
def technician_invoice_create(request):
    if request.method == 'POST':
        form = TechnicianInvoiceForm(request.POST)
        if form.is_valid():
            invoice = form.save(commit=False)
            if hasattr(request.user, 'technician_profile'):
                invoice.technician = request.user.technician_profile
            invoice.save()
            
            # Save Parts
            for part in form.cleaned_data.get('parts'):
                InvoiceItem.objects.create(
                    invoice=invoice, part=part, quantity=1, price_at_time_pkr=part.price_pkr
                )
            
            # Save Services
            for service in form.cleaned_data.get('services'):
                InvoiceService.objects.create(
                    invoice=invoice, service=service, worker_fee_at_time_pkr=service.worker_fee_pkr
                )
            
            # Simulate sending WhatsApp OTP
            print(f"*** SIMULATED WHATSAPP MESSAGE ***")
            print(f"To: {invoice.customer_phone}")
            print(f"Message: Your service invoice is ready. Your secure OTP is {invoice.otp_code}")
            print(f"Link: http://127.0.0.1:8000/invoice/{invoice.id}/")
            print(f"**********************************")

            return redirect('invoice_detail_view', pk=invoice.id)
    else:
        form = TechnicianInvoiceForm()
    return render(request, 'invoices/technician/form.html', {'form': form})

from django.contrib.admin.views.decorators import staff_member_required

def load_parts(request):
    category = request.GET.get('appliance')
    parts = ProductInventory.objects.filter(category=category).order_by('part_name')
    return render(request, 'invoices/partials/parts_options.html', {'parts': parts})

def verify_otp_view(request, pk):
    invoice = get_object_or_404(Invoice, id=pk)
    
    if request.method == 'POST':
        form = OTPVerificationForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['otp'] == invoice.otp_code:
                # Store verification in session
                request.session[f'verified_{invoice.id}'] = True
                invoice.otp_verified = True
                invoice.save()
                return redirect('invoice_detail_view', pk=invoice.id)
            else:
                form.add_error('otp', 'Invalid OTP code. Please check your WhatsApp.')
    else:
        form = OTPVerificationForm()
        
    return render(request, 'invoices/auth/otp_verify.html', {'form': form, 'invoice': invoice})

def invoice_detail_view(request, pk):
    invoice = get_object_or_404(Invoice, id=pk)
    
    # Check if OTP is verified in session
    if not request.session.get(f'verified_{invoice.id}'):
        return redirect('verify_otp_view', pk=invoice.id)
        
    has_feedback = hasattr(invoice, 'feedback')
    form = FeedbackForm() if not has_feedback else None
    return render(request, 'invoices/invoice_detail.html', {'invoice': invoice, 'form': form, 'has_feedback': has_feedback})

@staff_member_required
def custom_admin_dashboard(request):
    total_invoices_count = Invoice.objects.count()
    all_invoices = Invoice.objects.all()
    
    total_paid_amount = sum(inv.grand_total for inv in all_invoices if inv.otp_verified)
    total_pending_amount = sum(inv.grand_total for inv in all_invoices if not inv.otp_verified)
    active_customers = Invoice.objects.values('customer_phone').distinct().count()
    
    recent_invoices = all_invoices.order_by('-created_at')[:10]
    
    # Calculate Snapshot Data (Product Inventory counts by Category)
    inventory_counts = ProductInventory.objects.values('category').annotate(count=Count('id')).order_by('-count')[:4]
    
    # Calculate Chart Data (Monthly Revenue and Invoices)
    # For simplicity, let's aggregate invoices by month for the last 6 months
    from django.utils import timezone
    from datetime import timedelta
    six_months_ago = timezone.now() - timedelta(days=180)
    
    monthly_data = Invoice.objects.filter(created_at__gte=six_months_ago.replace(day=1)).annotate(
        month=TruncMonth('created_at')
    ).values('month').annotate(count=Count('id')).order_by('month')
    
    labels = []
    invoice_data = []
    revenue_data = []
    
    # Fill in actual revenue per month (requires calculating grand_total manually per invoice per month, or approximated)
    # Since grand_total is a property, we can't sum it in the DB query directly. We will group in python.
    monthly_stats = {}
    for inv in Invoice.objects.filter(created_at__gte=six_months_ago.replace(day=1)):
        m = inv.created_at.strftime('%b')
        if m not in monthly_stats:
            monthly_stats[m] = {'revenue': 0, 'count': 0}
        monthly_stats[m]['revenue'] += float(inv.grand_total)
        monthly_stats[m]['count'] += 1
        
    for m, stats in monthly_stats.items():
        labels.append(m)
        revenue_data.append(stats['revenue'])
        invoice_data.append(stats['count'])
        
    chart_json = json.dumps({
        'labels': labels,
        'revenue': revenue_data,
        'invoices': invoice_data
    })
    
    context = {
        'total_invoices': total_invoices_count,
        'total_paid': total_paid_amount,
        'total_pending': total_pending_amount,
        'active_customers': active_customers,
        'recent_invoices': recent_invoices,
        'inventory_counts': inventory_counts,
        'chart_json': chart_json,
        'title': "Digital Invoice Intelligence",
    }
    return render(request, 'invoices/admin/dashboard.html', context)

@user_passes_test(lambda u: u.is_superuser)
def admin_invoice_list(request):
    invoices = Invoice.objects.all().order_by('-created_at')
    return render(request, 'invoices/admin/invoice_list.html', {'invoices': invoices})

@user_passes_test(lambda u: u.is_superuser)
def admin_feedback_list(request):
    feedbacks = CustomerFeedback.objects.all().order_by('-submitted_at')
    return render(request, 'invoices/admin/feedback_list.html', {'feedbacks': feedbacks})

@user_passes_test(lambda u: u.is_superuser)
def admin_inventory_list(request):
    inventories = ProductInventory.objects.all().order_by('category', 'part_name')
    return render(request, 'invoices/admin/inventory_list.html', {'inventories': inventories})

@user_passes_test(lambda u: u.is_superuser)
def admin_service_list(request):
    services = ServiceType.objects.all().order_by('name')
    return render(request, 'invoices/admin/service_list.html', {'services': services})

@user_passes_test(lambda u: u.is_superuser)
def admin_technician_list(request):
    technicians = TechnicianProfile.objects.all().order_by('employee_id')
    return render(request, 'invoices/admin/technician_list.html', {'technicians': technicians})

@login_required(login_url='login_view')
def global_search_view(request):
    query = request.GET.get('q', '')
    invoice_results = []
    product_results = []
    
    if query:
        # Search invoices
        invoice_results = Invoice.objects.filter(
            Q(customer_name__icontains=query) |
            Q(customer_phone__icontains=query) |
            Q(id__icontains=query)
        )[:10]
        
        # Search products
        product_results = ProductInventory.objects.filter(
            Q(part_name__icontains=query) |
            Q(model_number__icontains=query) |
            Q(category__icontains=query)
        )[:10]
        
    context = {
        'query': query,
        'invoice_results': invoice_results,
        'product_results': product_results,
    }
    return render(request, 'invoices/search_results.html', context)

def submit_feedback_view(request, pk):
    invoice = get_object_or_404(Invoice, id=pk)
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.invoice = invoice
            feedback.save()
            return HttpResponse('<div class="alert alert-success fw-bold text-center mt-3">Thank You! Your feedback and technician verification have been recorded.</div>')
        return render(request, 'invoices/partials/survey_form.html', {'form': form, 'invoice': invoice})
    return HttpResponse("Invalid Method", status=400)
