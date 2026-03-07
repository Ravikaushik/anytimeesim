from django.core.management.base import BaseCommand
from esim_store.models import Country

class Command(BaseCommand):
    help = 'Check existing countries and add missing ones'

    def handle(self, *args, **options):
        # Check what countries we have
        countries = Country.objects.all().order_by('name')
        self.stdout.write(f'Current countries in database: {countries.count()}')
        
        for country in countries:
            self.stdout.write(f'{country.name} ({country.code})')
        
        # Check for specific missing countries
        missing_countries = [
            ('United Kingdom', 'GB'),
            ('United States', 'US'),
            ('United Arab Emirates', 'AE'),
        ]
        
        for country_name, country_code in missing_countries:
            if not Country.objects.filter(code=country_code).exists():
                self.stdout.write(f'Missing: {country_name} ({country_code})')
            else:
                self.stdout.write(f'Exists: {country_name} ({country_code})')