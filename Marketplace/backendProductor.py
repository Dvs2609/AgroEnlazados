from django.contrib.auth.backends import BaseBackend
from .models import Productor

class ProductorAuthenticationBackend(BaseBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        try:
            user = Productor.objects.get(email=email)
            if user.check_password(password):
                print("Usuario autenticado")
                return user
            else:
                print("Contraseña incorrecta")
        except Productor.DoesNotExist:
            print("Usuario no encontrado")

        return None

    def get_user(self, user_id):
        try:
            return Productor.objects.get(pk=user_id)
        except Productor.DoesNotExist:
            return None