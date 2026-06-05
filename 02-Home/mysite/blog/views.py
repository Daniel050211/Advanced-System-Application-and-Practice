from django.shortcuts import render, redirect
from .models import Entry
from .forms import EntryForm
import paho.mqtt.client as mqtt

# 1. Main Home Page Route
def index(request):
    return render(request, 'blog/index.html')

# 2. Blog Feed List Page Route
def blog(request):
    entries = Entry.objects.order_by('-date_posted') 
    context = {'entries' : entries}
    return render(request, 'blog/blog.html', context)

# 3. New Add Entry Form Page Route (Pages 74-78)
def add(request):
    if request.method == 'POST': 
        form = EntryForm(request.POST) # Grabs submission data
        if form.is_valid():
            form.save() # Automatically creates and saves database record row!
            return redirect('/blog/') # Jumps back to feed page
    else: 
        form = EntryForm() # Generates a clean empty text field input

    context = {'form' : form} 
    return render(request, 'blog/add.html', context)
def css_style(request):
   return render(request, 'blog/css_style.html')