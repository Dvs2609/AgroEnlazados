import pandas as pd
import os
import sys
import django
import googlemaps
from datetime import datetime
from django.utils.text import slugify

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "AgroEnlazados.settings")
django.setup()

df = pd.read_csv('Marketplace/data/listado-sociedades-cooperativas.csv', encoding='utf-8', sep=',')

gmaps = googlemaps.Client(key='AIzaSyDC7r4PCzv8FSMXhcqXKFLXObpn2t-ZyyI')

from Marketplace.models import Cooperativa, Provincia

def get_location(address):
    geocode_result = gmaps.geocode(address)
    if geocode_result:
        lat = geocode_result[0]['geometry']['location']['lat']
        lon = geocode_result[0]['geometry']['location']['lng']
        return lat, lon
    else:
        return None, None

def get_provincia_comunidad_id(provincia):
    try:
        provincia = Provincia.objects.get(provincia=provincia)
        comunidad_autonoma = provincia.comunidad_autonoma
        return provincia, comunidad_autonoma
    except Provincia.DoesNotExist:
        return None, None
    
def unique_slug_generator(instance, slug_field):
    model_class = instance.__class__
    unique_slug = slugify(getattr(instance, slug_field))
    counter = 1

    while model_class.objects.filter(slug=unique_slug).exists():
        unique_slug = f"{slugify(getattr(instance, slug_field))}-{counter}"
        counter += 1

    return unique_slug
for index, row in df.iterrows():
    address = f"{row['DENOMINACIÓN SOCIAL']}, {row['LOCALIDAD']}, {row['PROVINCIA']} {row['CP']}, Spain"
    provincia = row['PROVINCIA']#localidad
    provincia, comunidad_autonoma = get_provincia_comunidad_id(provincia)
    print(address)
    lat, lon = get_location(address)
    if lat is None and lon is None:
        address2 = f"{row['LOCALIDAD']}, {row['CP']}, Spain"
        lat, lon = get_location(address2)
        print(address2)
    #print(provincia)
    #print(comunidad_autonoma)
    fecha = pd.to_datetime(row['FECHA INSCRIPCIÓN'], format='%d/%m/%y')
    if provincia is not None and comunidad_autonoma is not None:
        cooperativa = Cooperativa(
            num_inscripcion=row['Nº INSCRIPCIÓN'],
            denominación_social=row['DENOMINACIÓN SOCIAL'],
            provincia_coop=provincia,
            localidad_coop=row['LOCALIDAD'],
            cp_coop=row['CP'],
            grado_coop=row['CLASE O GRADO'],
            fecha_inscripcion_coop=fecha.date() if not pd.isnull(fecha) else None,
            latitude=lat,
            longitude=lon,
            ccaa_coop=comunidad_autonoma,
        )
        cooperativa.slug = unique_slug_generator(cooperativa, 'denominación_social')
        cooperativa.save()