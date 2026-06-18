from openpyxl import Workbook

rows = [
    ("Category", "Model Number", "Part Name", "Part Code", "Price"),
    ("Refrigerator Compressor", "HRF-350X", "Compressor Assembly", "COMP-HRF350X-01", 14500.00),
    ("Refrigerator Door Gasket", "HRF-350X", "Door Gasket Seal", "GSK-HRF350X-02", 650.00),
    ("Washing Machine Drum", "HWM-6500", "Inner Drum", "DRM-HWM6500-03", 8200.00),
    ("Air Conditioner PCB", "HAC-09K", "Control PCB", "PCB-HAC09K-04", 3750.00),
]

wb = Workbook()
ws = wb.active
for r in rows:
    ws.append(r)
wb.save("mock_inventory.xlsx")
print("Wrote mock_inventory.xlsx")
