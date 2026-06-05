from django.shortcuts import render
from .models import InventoryItem
from django.utils import timezone
from datetime import timedelta
from django.db.models import Count  # Required for summary calculations

def index(request):
    # 1) Existing Assignment 1 Filters
    all_items = InventoryItem.objects.all()
    expensive_items = InventoryItem.objects.filter(unit_price__gt=4000)
    
    five_years_ago = timezone.now() - timedelta(days=5*365)
    old_items = InventoryItem.objects.filter(created_date__lt=five_years_ago)
    
    # 2) Assignment 1 Summaries: Group and Count by Type and Brand
 
    type_summary = InventoryItem.objects.values('item_type').annotate(total_count=Count('id')).order_by('-total_count')
    

    brand_summary = InventoryItem.objects.values('brand').annotate(total_count=Count('id')).order_by('-total_count')
    
    context = {
        'all_items': all_items,
        'expensive_items': expensive_items,
        'old_items': old_items,
        'type_summary': type_summary,   # Passed to HTML
        'brand_summary': brand_summary, # Passed to HTML
    }
    return render(request, 'inventory/index.html', context)