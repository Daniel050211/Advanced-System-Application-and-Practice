import os
import django
import xlrd
from datetime import datetime, timezone

# 1. Initialize the Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

# Import your inventory model
from inventory.models import InventoryItem

def run():
    excel_file_path = 'item_sample.xls'
    
    if not os.path.exists(excel_file_path):
        print(f"Error: Cannot find {excel_file_path} in this directory.")
        return

    print("Opening Excel spreadsheet...")
    # Open the workbook and select the very first sheet tab
    workbook = xlrd.open_workbook(excel_file_path)
    sheet = workbook.sheet_by_index(0)
    
    print(f"Found sheet '{sheet.name}' with {sheet.nrows} rows. Starting import...")
    
    count = 0
    # Loop through rows, starting at row 1 (skipping row 0 because it's the column titles header)
    for row_idx in range(1, sheet.nrows):
        # Extract row cells values cleanly
        item_no      = str(sheet.cell_value(row_idx, 0)).strip()
        item_type    = str(sheet.cell_value(row_idx, 1)).strip()
        name         = str(sheet.cell_value(row_idx, 2)).strip()
        description  = str(sheet.cell_value(row_idx, 3)).strip()
        brand        = str(sheet.cell_value(row_idx, 4)).strip()
        unit_price   = float(sheet.cell_value(row_idx, 5))
        stock        = int(sheet.cell_value(row_idx, 6))
        
        # Parse Excel's internal float date value safely into a standard timezone datetime object
        date_cell = sheet.cell(row_idx, 7)
        if date_cell.ctype == xlrd.XL_CELL_DATE:
            # Convert Excel date float to Python datetime tuple
            date_tuple = xlrd.xldate_as_tuple(date_cell.value, workbook.datemode)
            created_dt = datetime(*date_tuple).replace(tzinfo=timezone.utc)
        else:
            created_dt = datetime.now(timezone.utc)

        # Save or update structural items into our database table rows block
        InventoryItem.objects.update_or_create(
            item_no=item_no,
            defaults={
                'item_type': item_type,
                'name': name,
                'description': description,
                'brand': brand,
                'unit_price': unit_price,
                'stock': stock,
                'created_date': created_dt
            }
        )
        count += 1
        print(f" Loaded: {item_no} - {name}")
            
    print(f"\nSuccessfully imported {count} items directly from the native .xls file!")

if __name__ == '__main__':
    run()