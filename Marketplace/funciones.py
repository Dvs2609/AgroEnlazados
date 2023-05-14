import datetime
from django.contrib import messages
import re

# Funcion que convierte las querys a la BBDD en diccionarios, para acceder de manera mas facil al valor de cada campo en las templates
def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        {column: (row[i].isoformat() if isinstance(row[i], datetime.date) else row[i]) for i, column in enumerate(columns)}
        for row in cursor.fetchall()
    ]


def comprobarContraseña(request, pwd, pwdConf):
    if(len(pwd) < 8):
        messages.error(request, "La contraseña debe contener al menos 8 caracteres")
        return False # longitud corta

    if(pwd != pwdConf):
        messages.error(request, "Las contraseñas no coinciden")
        return False # false
    
    return True # true

def camposObligatoriosRellenos(request, id_regepa, dni, username, correo, pwd, pwdConf, cp):

    if len(id_regepa) == 0: # esto sigue en pruebas
        messages.error(request, "Hay id_regepa")
        return False
    return True