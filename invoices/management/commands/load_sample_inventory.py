from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Load sample ProductInventory rows for local testing.'

    def handle(self, *args, **options):
        try:
            from invoices.models import ProductInventory
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Could not import ProductInventory: {e}"))
            return

        samples = [
            {"category": "Refrigerator Compressor", "model_number": "HRF-350X", "part_name": "Compressor Assembly", "part_code": "COMP-HRF350X-01", "price_pkr": 14500.00},
            {"category": "Refrigerator Gasket", "model_number": "HRF-350X", "part_name": "Door Gasket Seal", "part_code": "GSK-HRF350X-02", "price_pkr": 650.00},
            {"category": "Washing Machine", "model_number": "HWM-6500", "part_name": "Inner Drum", "part_code": "DRM-HWM6500-03", "price_pkr": 8200.00},
            {"category": "Air Conditioner", "model_number": "HAC-09K", "part_name": "Control PCB", "part_code": "PCB-HAC09K-04", "price_pkr": 3750.00},
        ]

        created = 0
        updated = 0
        for s in samples:
            obj, was_created = ProductInventory.objects.update_or_create(
                part_code=s['part_code'],
                defaults={
                    'category': s['category'],
                    'model_number': s['model_number'],
                    'part_name': s['part_name'],
                    'price_pkr': s['price_pkr'],
                }
            )
            if was_created:
                created += 1
            else:
                updated += 1

        self.stdout.write(self.style.SUCCESS(f"Sample inventory loaded. Created: {created}, Updated: {updated}"))
