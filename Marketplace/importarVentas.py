import os
import sys
import json
import django

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "AgroEnlazados.settings")
django.setup()

from Marketplace.models import TipoVenta

with open('Marketplace/data/tipos_de_venta.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

ventas = data['ventas']

for venta in ventas:
    tipo_venta = TipoVenta(
        id_tipo_venta=venta['id_tipo_venta'],
        tipo_venta=venta['tipo_venta'],
        descripción_venta=venta['descripcion_venta'],
        ventajas_venta=venta['ventajas_venta'],
        desventajas_venta=venta['desventajas_venta'],
        normativa_venta=venta['normativa_venta'],
        inscripción_venta=venta['inscripcion_venta'],
    )
    tipo_venta.save()