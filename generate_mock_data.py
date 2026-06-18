import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tcm_project.settings')
django.setup()

from invoices.models import ProductInventory, ServiceType, Invoice

def create_mock_data():
    Invoice.objects.all().delete()
    ProductInventory.objects.all().delete()
    ServiceType.objects.all().delete()

    appliances = [
        "Refrigerator", "Air Conditioner", "Washing Machine", "Microwave Oven", 
        "Dishwasher", "Water Heater", "Television", "Water Purifier",
        "Vacuum Cleaner", "Air Purifier", "Deep Freezer", "Oven",
        "Coffee Maker", "Toaster", "Blender", "Food Processor",
        "Electric Kettle", "Juicer", "Induction Cooktop", "Chimney"
    ]

    parts_base = [
        "Compressor Assembly", "Control PCB", "Thermostat", "Motor",
        "Filter", "Heating Element", "Power Cord", "Sensor"
    ]

    services_list = [
        "General Inspection", "Deep Cleaning", "Gas Refill", "PCB Repair",
        "Motor Replacement", "Installation", "Uninstallation", "Filter Change",
        "Thermostat Calibration", "Compressor Servicing", "Leak Fix", "Noise Diagnosis",
        "Wiring Repair", "Panel Replacement", "Drum Cleaning", "Water Pump Repair",
        "Display Fix", "Switch Replacement", "Drainage Blockage Fix", "Full Servicing"
    ]

    print("Creating Appliances and Parts...")
    part_counter = 1
    for appliance in appliances:
        for i, part in enumerate(parts_base):
            part_name = f"{part} for {appliance}"
            part_code = f"PRT-{part_counter:04d}"
            price = 500 + (i * 1500)
            ProductInventory.objects.create(
                category=appliance,
                model_number=f"{appliance[:3].upper()}-X{i}",
                part_name=part_name,
                part_code=part_code,
                price_pkr=price
            )
            part_counter += 1

    print("Creating Services...")
    for i, service_name in enumerate(services_list):
        fee = 1000 + (i * 500)
        ServiceType.objects.create(
            name=service_name,
            description=f"Standard {service_name} procedure.",
            worker_fee_pkr=fee
        )

    print(f"Successfully generated {len(appliances)} appliances with parts, and {len(services_list)} services.")

if __name__ == '__main__':
    create_mock_data()
