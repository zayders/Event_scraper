
from django.urls import path
from . import views

urlpatterns = [    
    path('', views.event_list, name='event_list'),
    path('events_geojson/', views.events_geojson, name='events_geojson'),
    path('event-data/', views.event_data, name='event_data'),
    path('map/', views.map_view, name='map_view'),
]