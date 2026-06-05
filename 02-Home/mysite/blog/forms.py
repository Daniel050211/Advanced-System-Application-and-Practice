from django.forms import ModelForm
from .models import Entry

class EntryForm(ModelForm):
    class Meta:                   # Attach additional information
        model = Entry
        fields = ('text', )