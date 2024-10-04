from django.shortcuts import render
from django.http import JsonResponse
from .models import Event, Format

# Affiche la liste des événements avec leurs formats associés
# Utilise la méthode prefetch_related pour optimiser les requêtes liées aux formats
def event_list(request):
    events = Event.objects.all().prefetch_related('formats')
    return render(request, 'events/event_list.html', {'events': events})

# Affiche la page de la carte des événements sans charger de données spécifiques
def map_view(request):
    return render(request, 'events/map.html')

# Affiche une autre vue de la carte, map.html, pour visualiser les événements sur une carte
def event_map(request):
    return render(request, 'map.html')

# Génère une réponse GeoJSON avec les événements et leurs coordonnées géographiques
# Chaque événement est transformé en un objet GeoJSON "Feature" avec les propriétés (nom, date, url)
def events_geojson(request):
    events = Event.objects.all()
    features = []
    for event in events:
        feature = {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [event.longitude, event.latitude]  # Assurez-vous d'avoir ces champs dans votre modèle
            },
            "properties": {
                "name": event.name,
                "date": event.date.isoformat(),
                "url": event.url
            }
        }
        features.append(feature)

    geojson = {
        "type": "FeatureCollection",
        "features": features
    }
    
    return JsonResponse(geojson)

# Utilise l'API Adresse du gouvernement pour obtenir les coordonnées (latitude et longitude)
# à partir de la ville et du code postal. Renvoie None si aucune correspondance n'est trouvée
def get_coordinates(city, postal_code):
    base_url = "https://api-adresse.data.gouv.fr/search/"
    params = {
        'q': f'{postal_code} {city}',
        'limit': 1
    }
    response = requests.get(base_url, params=params)
    data = response.json()
    if data['features']:
        coordinates = data['features'][0]['geometry']['coordinates']
        return coordinates[1], coordinates[0]  # Retourne latitude, longitude
    else:
        return None, None

# Met à jour les coordonnées (latitude et longitude) des événements qui n'en ont pas encore
# Utilise la fonction get_coordinates pour obtenir les coordonnées via l'API du gouvernement
def update_event_coordinates():
    events = Event.objects.filter(latitude__isnull=True, longitude__isnull=True)

    for event in events:
        latitude, longitude = get_coordinates(event.city, event.postal_code)
        if latitude and longitude:
            event.latitude = latitude
            event.longitude = longitude
            event.save()
            print(f"Updated event {event.name} with coordinates ({latitude}, {longitude})")

# Renvoie une réponse JSON avec les données de tous les événements
# Inclut le nom, la date, le lieu, la latitude et la longitude, mais seulement pour les événements ayant des coordonnées
def event_data(request):
    events = Event.objects.all()
    data = [{
        'name': event.name,
        'date': event.date,
        'location': event.location,
        'latitude': event.latitude,
        'longitude': event.longitude,
    } for event in events if event.latitude and event.longitude]
    return JsonResponse(data, safe=False)
