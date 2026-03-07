from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from esim_store.models import Country, ESIMPlan

class Command(BaseCommand):
    help = 'Populate database with sample eSIM data'

    def handle(self, *args, **options):
        self.stdout.write('Creating sample data...')
        
        # Create countries
        countries_data = [
            {'name': 'United States', 'code': 'USA'},
            {'name': 'United Kingdom', 'code': 'UK'},
            {'name': 'Canada', 'code': 'CA'},
            {'name': 'Australia', 'code': 'AU'},
            {'name': 'Germany', 'code': 'DE'},
            {'name': 'France', 'code': 'FR'},
            {'name': 'Japan', 'code': 'JP'},
            {'name': 'Singapore', 'code': 'SG'},
            {'name': 'United Arab Emirates', 'code': 'AE'},
            {'name': 'Thailand', 'code': 'TH'},
            {'name': 'Spain', 'code': 'ES'},
            {'name': 'Italy', 'code': 'IT'},
        ]
        
        countries = {}
        for country_data in countries_data:
            country, created = Country.objects.get_or_create(
                name=country_data['name'],
                defaults={'code': country_data['code']}
            )
            countries[country.code] = country
            if created:
                self.stdout.write(f'Created country: {country.name}')
        
        # Create eSIM plans
        plans_data = [
            {
                'name': 'USA 1GB 7 Days',
                'price': 9.99,
                'data_amount': '1GB',
                'validity_days': 7,
                'countries': ['USA'],
                'description': 'Perfect for short trips to the USA'
            },
            {
                'name': 'USA 5GB 30 Days',
                'price': 24.99,
                'data_amount': '5GB',
                'validity_days': 30,
                'countries': ['USA'],
                'description': 'Great for extended stays in the USA'
            },
            {
                'name': 'USA 10GB 30 Days',
                'price': 39.99,
                'data_amount': '10GB',
                'validity_days': 30,
                'countries': ['USA'],
                'description': 'Best value for USA connectivity'
            },
            {
                'name': 'UK 1GB 7 Days',
                'price': 8.99,
                'data_amount': '1GB',
                'validity_days': 7,
                'countries': ['UK'],
                'description': 'Stay connected in the UK'
            },
            {
                'name': 'UK 3GB 15 Days',
                'price': 19.99,
                'data_amount': '3GB',
                'validity_days': 15,
                'countries': ['UK'],
                'description': 'Mid-range UK plan'
            },
            {
                'name': 'UK 8GB 30 Days',
                'price': 34.99,
                'data_amount': '8GB',
                'validity_days': 30,
                'countries': ['UK'],
                'description': 'Full month UK coverage'
            },
            {
                'name': 'Canada 2GB 10 Days',
                'price': 12.99,
                'data_amount': '2GB',
                'validity_days': 10,
                'countries': ['CA'],
                'description': 'Explore Canada with ease'
            },
            {
                'name': 'Canada 6GB 30 Days',
                'price': 29.99,
                'data_amount': '6GB',
                'validity_days': 30,
                'countries': ['CA'],
                'description': 'Extended Canada stay'
            },
            {
                'name': 'Australia 1GB 7 Days',
                'price': 10.99,
                'data_amount': '1GB',
                'validity_days': 7,
                'countries': ['AU'],
                'description': 'Australian adventure starter'
            },
            {
                'name': 'Australia 4GB 21 Days',
                'price': 27.99,
                'data_amount': '4GB',
                'validity_days': 21,
                'countries': ['AU'],
                'description': 'Explore the land down under'
            },
            {
                'name': 'Europe 3GB 15 Days',
                'price': 22.99,
                'data_amount': '3GB',
                'validity_days': 15,
                'countries': ['UK', 'DE', 'FR', 'ES', 'IT'],
                'description': 'Multi-country European plan'
            },
            {
                'name': 'Europe 10GB 30 Days',
                'price': 49.99,
                'data_amount': '10GB',
                'validity_days': 30,
                'countries': ['UK', 'DE', 'FR', 'ES', 'IT'],
                'description': 'Complete European coverage'
            },
            {
                'name': 'Asia 2GB 14 Days',
                'price': 15.99,
                'data_amount': '2GB',
                'validity_days': 14,
                'countries': ['JP', 'SG', 'TH'],
                'description': 'Asian connectivity solution'
            },
            {
                'name': 'Asia 7GB 30 Days',
                'price': 37.99,
                'data_amount': '7GB',
                'validity_days': 30,
                'countries': ['JP', 'SG', 'TH'],
                'description': 'Extended Asian stay'
            },
            {
                'name': 'Worldwide 5GB 30 Days',
                'price': 59.99,
                'data_amount': '5GB',
                'validity_days': 30,
                'countries': ['USA', 'UK', 'CA', 'AU', 'DE', 'FR', 'JP', 'SG', 'AE', 'TH', 'ES', 'IT'],
                'description': 'Global connectivity for world travelers'
            },
            {
                'name': 'Worldwide 15GB 30 Days',
                'price': 89.99,
                'data_amount': '15GB',
                'validity_days': 30,
                'countries': ['USA', 'UK', 'CA', 'AU', 'DE', 'FR', 'JP', 'SG', 'AE', 'TH', 'ES', 'IT'],
                'description': 'Premium global plan for heavy users'
            },
        ]
        
        for plan_data in plans_data:
            plan, created = ESIMPlan.objects.get_or_create(
                name=plan_data['name'],
                defaults={
                    'price': plan_data['price'],
                    'data_amount': plan_data['data_amount'],
                    'validity_days': plan_data['validity_days'],
                    'description': plan_data['description'],
                }
            )
            
            if created:
                # Add countries to the plan
                for country_code in plan_data['countries']:
                    if country_code in countries:
                        plan.countries.add(countries[country_code])
                self.stdout.write(f'Created plan: {plan.name}')
        
        self.stdout.write(
            self.style.SUCCESS('Successfully populated database with sample data')
        )