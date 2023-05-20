import os
import django
import chardet
import sys
import codecs
from django.core.management import call_command
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "AgroEnlazados.settings")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "AgroEnlazados.settings")
django.setup()

rawdata = open('datadump.json', 'rb').read()
result = chardet.detect(rawdata)
char_encoding = result['encoding']
print(char_encoding)

with open('datadump.json', 'r', encoding='utf-16') as f:
    data = f.read()

with open('datadump_utf8.json', 'w', encoding='utf-8') as f:
    f.write(data)

with codecs.open('datadump.json', 'w', 'utf-8') as f:
    call_command('dumpdata', stdout=f)
"""
import chardet    
rawdata = open('datadump.json', 'rb').read()
result = chardet.detect(rawdata)
char_encoding = result['encoding']
print(char_encoding)"""