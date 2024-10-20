from django.core.management.base import BaseCommand
from events.models import Event
import re


# Le champ Location contient du texte : CODE POSTAL + NOM DE LA VILLE
# Cette commande scinde les deux dans deux champs ! City et Postal_code
class Command(BaseCommand):
    help = 'Update city and postal code for events based on location'

    def handle(self, *args, **kwargs):
        events = Event.objects.all()
        for event in events:
            # Extraction du code postal et de la ville à partir de location
            match = re.match(r"(\d{5})\s(.+)", event.location)
            if match:
                postal_code, city = match.groups()
                event.postal_code = postal_code
                event.city = city
                event.save()
                self.stdout.write(self.style.SUCCESS(f"Updated Event ID {event.id} with city {city} and postal code {postal_code}"))
            else:
                self.stdout.write(self.style.WARNING(f"Could not parse location for Event ID {event.id}: {event.location}"))
