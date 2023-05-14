import pandas as pd
import os
import sys
import django
import googlemaps
import json

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "AgroEnlazados.settings")
django.setup()

with open('Marketplace/data/ferias_y_mercadillos.json', encoding='utf-8') as json_file:
    data = json.load(json_file)

gmaps = googlemaps.Client(key='AIzaSyDC7r4PCzv8FSMXhcqXKFLXObpn2t-ZyyI')

from Marketplace.models import FeriaMercadillo, Provincia, ComunidadAutonoma

def get_location(address):
    geocode_result = gmaps.geocode(address)
    if geocode_result:
        lat = geocode_result[0]['geometry']['location']['lat']
        lon = geocode_result[0]['geometry']['location']['lng']
        return lat, lon
    else:
        return None, None
    
def get_comunidad_autonoma(name):
    comunidad = ComunidadAutonoma.objects.filter(nombre=name).first()
    return comunidad

for row in data:
    address = f"{row['Ubicación']}, {row['Provincia']}, Spain"
    print(address)
    lat, lon = get_location(address)
    
    provincia = Provincia.objects.filter(provincia=row['Provincia']).first()    
    comunidad = get_comunidad_autonoma(row.get("Comunidad", None))

    nombre = row.get("Nombre", None)
    dias = row.get("Dia de Mercadillo", None)
    tipo = row.get("Tipo", None)
    ubicacion = row.get("Ubicación", None)
    horario = row.get("Horario", None)
    puestos = row.get("Puestos", None)
    descripcion = row.get("Descripción", None)
    

    if provincia is not None:
        feria_mercadillo = FeriaMercadillo(
            nombre_fm=nombre,
            días_fm=dias,
            tipo_fm=tipo,
            provincia_fm=provincia,
            ubicación_fm=ubicacion,
            horario_fm=horario,
            num_puestos_fm=puestos,
            descripción_fm=descripcion,
            ccaa_fm=comunidad,
            latitude_fm=lat,
            longitude_fm=lon,
        )
        feria_mercadillo.save()