import os
import sys
import django

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "AgroEnlazados.settings")
django.setup()

from Marketplace.models import ComunidadAutonoma, Provincia

# Creamos la comunidad autónoma de Extremadura
extremadura = ComunidadAutonoma.objects.create(nombre='Extremadura')

# Creamos las provincias asociadas a la comunidad autónoma
caceres = Provincia.objects.create(provincia='CACERES', comunidad_autonoma=extremadura)
badajoz = Provincia.objects.create(provincia='BADAJOZ', comunidad_autonoma=extremadura)