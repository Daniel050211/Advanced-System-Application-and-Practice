from django.shortcuts import render
from . import iot_mqtt
from django.db.models import Avg, Max, Min
from .models import Event
# Create your views here.
def index(request):
    events = Event.objects.order_by('-date_created')
    context = {'event_list' : events}
    return render(request, 'iot/index.html', context)

def log(request):
    # Fetch ALL events sorted by newest date record first
    all_events = Event.objects.order_by('-date_created')

    context = {
        'historical_events': all_events
    }
    return render(request, 'iot/log.html', context)

def info(request):
    # Group database data by location, then compute Max, Min, Avg for each distinct location
    summary_stats = Event.objects.values('node_loc').annotate(
        max_temp=Max('temp'),
        min_temp=Min('temp'),
        avg_temp=Avg('temp'),
        latest_id=Max('id'),
        latest_node=Max('node_id'),
        # 🚨 NEW: Retrieve the latest timestamp for each specific device group location
        latest_date=Max('date_created')
    )
    
    # Get overall pipeline last updated timestamp
    last_updated_entry = Event.objects.order_by('-date_created').first()
    last_updated = last_updated_entry.date_created if last_updated_entry else "No data available"
    
    context = {
        'summary_stats': summary_stats,
        'last_updated': last_updated
    }
    
    return render(request, 'iot/info.html', context)