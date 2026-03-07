from django.core.management.base import BaseCommand
from esim_store.models import Country

class Command(BaseCommand):
    help = 'Fix country codes to use proper ISO codes'

    def handle(self, *args, **options):
        # Fix United Kingdom code from UK to GB
        try:
            uk_country = Country.objects.get(code='UK')
            uk_country.code = 'GB'
            uk_country.save()
            self.stdout.write('Fixed United Kingdom code from UK to GB')
        except Country.DoesNotExist:
            self.stdout.write('United Kingdom not found with code UK')
        
        # Fix United States code from USA to US
        try:
            us_country = Country.objects.get(code='USA')
            us_country.code = 'US'
            us_country.save()
            self.stdout.write('Fixed United States code from USA to US')
        except Country.DoesNotExist:
            self.stdout.write('United States not found with code USA')
        
        self.stdout.write('Country codes updated successfully')