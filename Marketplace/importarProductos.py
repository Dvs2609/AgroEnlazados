import os
import sys
import csv
import django

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "AgroEnlazados.settings")
django.setup()

from Marketplace.models import Producto

with open('Marketplace/data/productos.csv', 'r', encoding='utf-8') as file:
    csv_reader = csv.reader(file)
    for row in csv_reader:
        producto = Producto(nombre=row[0])
        producto.save()