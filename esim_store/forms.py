from django import forms
from .models import ESIMPlan, Country
import pandas as pd

class ExcelImportForm(forms.Form):
    excel_file = forms.FileField(
        label='Upload Excel File',
        help_text='Excel file must have columns: name, price, data_amount, validity_days, countries (comma-separated country codes)'
    )

class BulkDeleteForm(forms.Form):
    confirm = forms.BooleanField(
        label='I understand this will delete ALL existing plans',
        help_text='This action cannot be undone. All plans will be permanently deleted.'
    )