import requests
from django.core.management.base import BaseCommand
from events.models import Event

class Command(BaseCommand):
    help = 'Update latitude and longitude for events based on city and postal code using the API Adresse'

    def handle(self, *args, **kwargs):
        events = Event.objects.all()
        for event in events:
            if event.city and event.postal_code:
                query = f'{event.postal_code} {event.city}'
                response = requests.get(f'https://api-adresse.data.gouv.fr/search/?q={query}')
                if response.status_code == 200:
                    data = response.json()
                    if data['features']:
                        coordinates = data['features'][0]['geometry']['coordinates']
                        event.longitude = coordinates[0]
                        event.latitude = coordinates[1]
                        event.save()
                        self.stdout.write(self.style.SUCCESS(f'Updated Event ID {event.id} with coordinates: {coordinates}'))
                    else:
                        self.stdout.write(self.style.WARNING(f'No coordinates found for Event ID {event.id}: {query}'))
                else:
                    self.stdout.write(self.style.ERROR(f'Failed to retrieve data for Event ID {event.id}: {query}'))
            else:
                self.stdout.write(self.style.WARNING(f'Missing city or postal code for Event ID {event.id}'))
