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


from Marketplace.models import FeriaMercadillo, Provincia, ComunidadAutonoma

def get_comunidad_autonoma(name):
    comunidad = ComunidadAutonoma.objects.filter(nombre=name).first()
    return comunidad

for row in data:
    address = f"{row['Ubicación']}, {row['Provincia']}, Spain"
    print(address)
    
    provincia = Provincia.objects.filter(provincia=row['Provincia']).first()
    comunidad = get_comunidad_autonoma(row.get("Comunidad", None))

    nombre = row.get("Nombre", None)
    dias = row.get("Dia de Mercadillo", None)
    tipo = row.get("Tipo", None)
    ubicacion = row.get("Ubicación", None)
    horario = row.get("Horario", None)
    puestos = row.get("Puestos", None)
    descripcion = row.get("Descripción", None)

    if isinstance(puestos, str) and puestos.isdigit():
        num_puestos_fm = int(puestos)
    else:
        num_puestos_fm = None
    
    if provincia is not None:
        feria_mercadillo = FeriaMercadillo(
            nombre_fm=nombre,
            días_fm=dias,
            tipo_fm=tipo,
            provincia_fm=provincia,
            ubicación_fm=ubicacion,
            horario_fm=horario,
            num_puestos_fm=num_puestos_fm,
            descripción_fm=descripcion,
            ccaa_fm=comunidad,
        )
        feria_mercadillo.save()
