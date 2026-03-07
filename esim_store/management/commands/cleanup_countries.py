from django.core.management.base import BaseCommand
from esim_store.models import Country

class Command(BaseCommand):
    help = 'Clean up duplicate countries and add missing ones'

    def handle(self, *args, **options):
        # First, let's see what countries we have
        countries = Country.objects.all()
        self.stdout.write(f'Current countries in database: {countries.count()}')
        
        # Check for duplicates by name
        names = {}
        for country in countries:
            if country.name in names:
                self.stdout.write(f'Duplicate found: {country.name} (code: {country.code}, existing: {names[country.name]})')
                # Delete the duplicate
                country.delete()
                self.stdout.write(f'Deleted duplicate: {country.name} ({country.code})')
            else:
                names[country.name] = country.code
        
        self.stdout.write(f'After cleanup: {Country.objects.count()} countries')
        
        # Now add missing countries
        countries_data = [
            ('United Kingdom', 'GB'),
            ('United States', 'US'),
            ('United Arab Emirates', 'AE'),
        ]
        
        for country_name, country_code in countries_data:
            if not Country.objects.filter(code=country_code).exists():
                Country.objects.create(code=country_code, name=country_name)
                self.stdout.write(f'Added: {country_name} ({country_code})')
            else:
                self.stdout.write(f'Already exists: {country_name} ({country_code})')
        
        self.stdout.write(f'Final count: {Country.objects.count()} countries')