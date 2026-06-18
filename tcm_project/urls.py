from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('', RedirectView.as_view(url='/technician/create/', permanent=False), name='index'),
    path('', include('invoices.urls')),
    path('admin/', admin.site.urls),
]
