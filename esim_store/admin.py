from django.contrib import admin
from django import forms
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import path
from django.http import HttpResponseRedirect
from django.utils.html import format_html
from .models import Country, ESIMPlan, PageContent, Order
from .forms import ExcelImportForm, BulkDeleteForm
import pandas as pd

@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ['name', 'code']
    search_fields = ['name', 'code']
    ordering = ['name']

@admin.register(ESIMPlan)
class ESIMPlanAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'data_amount', 'validity_days', 'is_active', 'country_list']
    list_filter = ['is_active', 'countries', 'price']
    search_fields = ['name', 'data_amount']
    filter_horizontal = ['countries']
    readonly_fields = ['created_at']
    actions = ['bulk_delete_plans']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'price', 'data_amount', 'validity_days', 'description', 'is_active')
        }),
        ('Media', {
            'fields': ('image',)
        }),
        ('Countries', {
            'fields': ('countries',)
        }),
        ('Metadata', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        })
    )
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('import-excel/', self.admin_site.admin_view(self.import_excel_view), name='esim_store_import_excel'),
            path('bulk-delete/', self.admin_site.admin_view(self.bulk_delete_view), name='esim_store_bulk_delete'),
            path('admin-tools/', self.admin_site.admin_view(self.admin_tools_view), name='esim_store_admin_tools'),
        ]
        return custom_urls + urls
    
    def changelist_view(self, request, extra_context=None):
        # Add context for custom buttons
        if extra_context is None:
            extra_context = {}
        extra_context['show_import_button'] = True
        extra_context['show_bulk_delete_button'] = True
        return super().changelist_view(request, extra_context=extra_context)
    
    def import_excel_view(self, request):
        if request.method == 'POST':
            form = ExcelImportForm(request.POST, request.FILES)
            if form.is_valid():
                try:
                    excel_file = request.FILES['excel_file']
                    df = pd.read_excel(excel_file)
                    
                    # Validate required columns with flexible naming
                    required_keywords = {
                        'name': ['name', 'data plan name', 'plan name', 'plan'],
                        'price': ['price', 'price (usd)', 'price usd', 'cost'],
                        'data_amount': ['data_amount', 'data amount', 'data', 'data type'],
                        'validity_days': ['validity_days', 'validity', 'validity days', 'days'],
                        'countries': ['countries', 'country', 'country code', 'country codes']
                    }
                    
                    # Find actual column names in the Excel file
                    column_mapping = {}
                    for key, possible_names in required_keywords.items():
                        found = False
                        for possible_name in possible_names:
                            if possible_name.lower() in [col.lower() for col in df.columns]:
                                # Get the exact column name from the file
                                actual_col = next(col for col in df.columns if col.lower() == possible_name.lower())
                                column_mapping[key] = actual_col
                                found = True
                                break
                        if not found:
                            messages.error(request, f'Excel file must contain a column for {key}. Try: {", ".join(possible_names)}')
                            return redirect('admin:esim_store_import_excel')
                    
                    created_count = 0
                    updated_count = 0
                    error_count = 0
                    
                    for index, row in df.iterrows():
                        try:
                            # Get or create plan using mapped column names
                            plan, created = ESIMPlan.objects.get_or_create(
                                name=row[column_mapping['name']],
                                defaults={
                                    'price': row[column_mapping['price']],
                                    'data_amount': row[column_mapping['data_amount']],
                                    'validity_days': row[column_mapping['validity_days']],
                                    'description': row.get('description', ''),
                                    'is_active': row.get('is_active', True)
                                }
                            )
                            
                            if not created:
                                # Update existing plan
                                plan.price = row[column_mapping['price']]
                                plan.data_amount = row[column_mapping['data_amount']]
                                plan.validity_days = row[column_mapping['validity_days']]
                                plan.description = row.get('description', '')
                                plan.is_active = row.get('is_active', True)
                                plan.save()
                                updated_count += 1
                            else:
                                created_count += 1
                            
                            # Handle countries
                            if pd.notna(row[column_mapping['countries']]):
                                country_codes = [code.strip() for code in str(row[column_mapping['countries']]).split(',')]
                                for code in country_codes:
                                    try:
                                        country = Country.objects.get(code=code.upper())
                                        plan.countries.add(country)
                                    except Country.DoesNotExist:
                                        messages.warning(request, f'Country code "{code}" not found for plan "{row[column_mapping["name"]]}"')
                        
                        except Exception as e:
                            error_count += 1
                            messages.warning(request, f'Error processing row {index + 1}: {str(e)}')
                    
                    messages.success(request, f'Import completed: {created_count} created, {updated_count} updated, {error_count} errors')
                    return redirect('admin:esim_store_esimplan_changelist')
                    
                except Exception as e:
                    messages.error(request, f'Error reading Excel file: {str(e)}')
        else:
            form = ExcelImportForm()
        
        context = {
            'form': form,
            'title': 'Import Plans from Excel',
            'opts': self.model._meta,
        }
        return render(request, 'admin/esim_store/esimplan/import_excel.html', context)
    
    def bulk_delete_view(self, request):
        current_count = ESIMPlan.objects.count()
        
        if request.method == 'POST':
            form = BulkDeleteForm(request.POST)
            if form.is_valid() and form.cleaned_data['confirm']:
                deleted_count = ESIMPlan.objects.count()
                ESIMPlan.objects.all().delete()
                messages.success(request, f'Successfully deleted {deleted_count} plans')
                return redirect('admin:esim_store_esimplan_changelist')
        else:
            form = BulkDeleteForm()
        
        context = {
            'form': form,
            'title': 'Bulk Delete All Plans',
            'opts': self.model._meta,
            'current_count': current_count,
        }
        return render(request, 'admin/esim_store/esimplan/bulk_delete.html', context)
    
    def get_actions(self, request):
        actions = super().get_actions(request)
        # Remove default delete action to replace with our custom one
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions
    
    def bulk_delete_plans(self, request, queryset):
        selected_count = queryset.count()
        if selected_count > 0:
            queryset.delete()
            messages.success(request, f'Successfully deleted {selected_count} selected plans')
    bulk_delete_plans.short_description = "Delete selected plans"
    
    def country_list(self, obj):
        return ", ".join([country.name for country in obj.countries.all()])
    country_list.short_description = "Countries"
    
    def admin_tools_view(self, request):
        from .models import Country, Order
        
        context = {
            'title': 'Admin Tools',
            'opts': self.model._meta,
            'plan_count': ESIMPlan.objects.count(),
            'country_count': Country.objects.count(),
            'active_orders': Order.objects.filter(status='pending').count(),
            'total_orders': Order.objects.count(),
        }
        return render(request, 'admin/esim_store/admin_tools.html', context)

@admin.register(PageContent)
class PageContentAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'is_active']
    list_filter = ['is_active']
    search_fields = ['title', 'slug']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'email', 'phone', 'esim_plan', 'order_date', 'status']
    list_filter = ['status', 'order_date', 'esim_plan']
    search_fields = ['name', 'email', 'phone']
    readonly_fields = ['order_date']
    
    fieldsets = (
        ('Customer Information', {
            'fields': ('name', 'email', 'phone')
        }),
        ('Order Details', {
            'fields': ('esim_plan', 'status')
        }),
        ('Metadata', {
            'fields': ('order_date',),
            'classes': ('collapse',)
        })
    )
