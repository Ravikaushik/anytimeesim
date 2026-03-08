from django.core.management.base import BaseCommand
from django.core.management import call_command
import os

class Command(BaseCommand):
    help = 'Auto setup: collect static files and add countries'

    def handle(self, *args, **options):
        self.stdout.write('Starting auto setup...')
        
        # Collect static files
        self.stdout.write('Collecting static files...')
        call_command('collectstatic', '--noinput', '--clear')
        self.stdout.write(self.style.SUCCESS('Static files collected successfully'))
        
        # Add all countries
        self.stdout.write('Adding countries to database...')
        call_command('add_all_countries')
        self.stdout.write(self.style.SUCCESS('Countries added successfully'))
        
        self.stdout.write(self.style.SUCCESS('Auto setup completed!'))