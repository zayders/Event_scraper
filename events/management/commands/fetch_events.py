import re
from django.core.management.base import BaseCommand
from events.models import Event, Format
import requests
from bs4 import BeautifulSoup

# URL de base
base_url = "https://fftri.t2area.com/calendrier.html"

#Nombre d'evenements maximum à récupérer
def get_event_count():
    page = requests.get(base_url)
    content = page.text
    soup1 = BeautifulSoup(content, 'html.parser')
    result = int(soup1.find('span', class_="js-adv-filter__results-count").text)
    return result

# Fonction pour récupérer les données d'une page spécifique
def fetch_data(limit_start):
    params = {'limitstart': limit_start}
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        return response.text
    else:
        print(f"Failed to retrieve data for limitstart={limit_start}")
        return None

class Command(BaseCommand):
    help = 'Fetch events from FFTRI website'

    def handle(self, *args, **kwargs):
        result = get_event_count()
        all_links = []
        for i in range(0, result, 10):
            print(f"Fetching page with limitstart={i}")
            page_data = fetch_data(i) 
            if page_data:
                soup = BeautifulSoup(page_data, 'html.parser')

                list_events = soup.find('ul', id="adv-filter-gallery")
                events = list_events.find_all('li')

                for event in events:
                    # Extraire les informations de l'événement
                    headline = event.find('h4', class_='stories__headline')
                    link = headline.find('a')
                    href = link['href']
                    name = link.text

                    # Trouver la date
                    date = event.find('time')['datetime']

                    # Trouver le lieu
                    metadata = event.find('p', class_='stories__metadata')
                    location_span = metadata.find_all('span')[2]
                    location = location_span.text.strip()

                    # Extraction du code postal et de la ville
                    match = re.match(r"(\d{5})\s(.+)", location)
                    if match:
                        postal_code = match.group(1)
                        city = match.group(2)
                    else:
                        postal_code = ''
                        city = location  # Si la regex ne correspond pas, on met toute la chaîne comme ville

                    # Créer ou mettre à jour l'événement
                    event_obj, created = Event.objects.update_or_create(
                        name=name,
                        date=date,
                        defaults={'location': location, 'link': href},
                        city=city,
                        postal_code=postal_code
                    )

                    # Trouver les formats et distances
                    trials = event.find_all('a', class_="trial")
                    for trial in trials:
                        distance = trial.find("div", class_="distance").text
                        format = trial.find("div", class_="format").text

                        # Créer ou obtenir le format sans dupliquer
                        format_obj, created = Format.objects.get_or_create(
                            distance=distance,
                            defaults={'format': format},
                        )

                        # Ajouter le format à l'événement
                        event_obj.formats.add(format_obj)

        print("Data fetching and updating completed.")