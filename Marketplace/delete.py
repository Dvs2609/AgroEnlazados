import os
import sys
import django

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "AgroEnlazados.settings")
django.setup()

from Marketplace.models import TipoVenta

# Eliminar todos los registros de TipoVenta
TipoVenta.objects.all().delete()
