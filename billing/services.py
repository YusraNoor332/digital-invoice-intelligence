import openpyxl
from decimal import Decimal, InvalidOperation
from django.db import transaction
from .models import ProductInventory

def ingest_inventory_from_excel(file_path_or_stream):
    """
    Reads an uploaded Excel file (.xlsx) and updates the ProductInventory model.
    Expected Columns: Category, Model Number, Part Name, Part Code, Price
    """
    try:
        workbook = openpyxl.load_workbook(file_path_or_stream, data_only=True)
        sheet = workbook.active
        
        # Assume the first row is the header
        header = [str(cell.value).strip().lower() for cell in sheet[1]]
        
        # Verify required columns exist
        required_cols = ['category', 'model number', 'part name', 'part code', 'price']
        for col in required_cols:
            if col not in header:
                raise ValueError(f"Missing required column: {col}")

        # Map column names to indices
        col_indices = {col_name: header.index(col_name) for col_name in required_cols}

        records_processed = 0
        records_updated = 0
        records_created = 0

        with transaction.atomic():
            # Iterate through rows starting from the second row
            for row in sheet.iter_rows(min_row=2, values_only=True):
                category = row[col_indices['category']]
                model_number = row[col_indices['model number']]
                part_name = row[col_indices['part name']]
                part_code = row[col_indices['part code']]
                price_raw = row[col_indices['price']]

                # Skip empty rows
                if not all([category, model_number, part_name, part_code]):
                    continue

                try:
                    price_pkr = Decimal(str(price_raw))
                except (InvalidOperation, TypeError, ValueError):
                    # Handle invalid price format gracefully
                    continue

                # Update or create the inventory item based on unique part_code
                obj, created = ProductInventory.objects.update_or_create(
                    part_code=str(part_code).strip(),
                    defaults={
                        'category': str(category).strip(),
                        'model_number': str(model_number).strip(),
                        'part_name': str(part_name).strip(),
                        'price_pkr': price_pkr,
                    }
                )
                
                records_processed += 1
                if created:
                    records_created += 1
                else:
                    records_updated += 1
                    
        return {
            'success': True,
            'processed': records_processed,
            'created': records_created,
            'updated': records_updated,
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }
