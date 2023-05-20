from django.db import models
from django.contrib.auth.models import UserManager
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.conf import settings
from django.template.defaultfilters import slugify
from django.db import IntegrityError

class ComunidadAutonoma(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nombre

class Provincia(models.Model):
    provincia = models.CharField(max_length=100, unique=True)
    comunidad_autonoma = models.ForeignKey(ComunidadAutonoma, on_delete=models.CASCADE, related_name='provincias')

    def __str__(self):
        return self.provincia
     
class Cooperativa(models.Model):
    id_coop = models.AutoField(primary_key=True)
    num_inscripcion = models.CharField(max_length=200)
    denominación_social = models.CharField(max_length=200)
    provincia_coop = models.ForeignKey(Provincia, on_delete=models.CASCADE)
    localidad_coop = models.CharField(max_length=200)
    cp_coop = models.CharField(max_length=10)
    grado_coop = models.CharField(max_length=200)
    fecha_inscripcion_coop = models.DateField()
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    ccaa_coop = models.ForeignKey(ComunidadAutonoma, on_delete=models.CASCADE)
    slug = models.SlugField(unique=True, blank=True, max_length=200)

    def save(self, *args, **kwargs):
        if not self.slug:
            original_slug = slugify(self.denominación_social)
            self.slug = original_slug

            # Intenta guardar el objeto. Si falla debido a un valor de slug duplicado,
            # agrega un número al final del slug e intenta nuevamente.
            for i in range(1, 1000):
                try:
                    super(Cooperativa, self).save(*args, **kwargs)
                    break
                except IntegrityError as e:
                    if 'Marketplace_cooperativa_slug_key' in str(e):
                        self.slug = f"{original_slug}-{i}"
                    else:
                        raise e
        else:
            super(Cooperativa, self).save(*args, **kwargs)

class FeriaMercadillo(models.Model):
    id_fm = models.AutoField(primary_key=True)
    nombre_fm = models.CharField(max_length=100)
    días_fm = models.CharField(max_length=100)
    tipo_fm = models.CharField(max_length=100, null=True)
    provincia_fm = models.ForeignKey(Provincia, on_delete=models.CASCADE)
    ubicación_fm = models.CharField(max_length=300)
    horario_fm = models.CharField(max_length=100, null=True)
    num_puestos_fm = models.IntegerField(null=True)
    descripción_fm = models.TextField(null=True)
    ccaa_fm = models.ForeignKey(ComunidadAutonoma, on_delete=models.CASCADE)
    latitude_fm = models.FloatField(null=True, blank=True)
    longitude_fm = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.nombre_fm

class TipoVenta(models.Model):
    id_tipo_venta = models.AutoField(primary_key=True)
    tipo_venta = models.CharField(max_length=100)
    descripción_venta = models.TextField()
    ventajas_venta = models.TextField()
    desventajas_venta = models.TextField()
    normativa_venta = models.TextField()
    inscripción_venta = models.TextField()

    def __str__(self):
        return self.tipo_venta


    
class ProductorManager(BaseUserManager):
    def create_user(self, id_regepa, dni_prod, email, password=None, **extra_fields):
        if not id_regepa:
            raise ValueError('El ID RegEPA debe ser establecido')
        if not dni_prod:
            raise ValueError('El DNI del productor debe ser establecido')
        if not email:
            raise ValueError('El email del productor debe ser establecido')
        email = self.normalize_email(email)
        user = self.model(id_regepa=id_regepa, dni_prod=dni_prod, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, id_regepa, dni_prod, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(id_regepa, dni_prod, email, password, **extra_fields)
    

class Producto(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class Productor(AbstractBaseUser, PermissionsMixin):
    id_regepa = models.CharField(max_length=10, unique=True)
    dni_prod = models.CharField(max_length=10)
    nombre_prod = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    productos_prod = models.ManyToManyField(Producto, blank=True, related_name='productores')
    provincia_prod = models.ForeignKey(Provincia, on_delete=models.CASCADE)
    ccaa_prod = models.ForeignKey(ComunidadAutonoma, on_delete=models.CASCADE)
    cp_prod = models.CharField(max_length=10, null=True, blank=True)
    username = models.CharField(max_length=50, null=True, blank=True)
    teléfono_prod = models.CharField(max_length=20, null=True, blank=True)
    tipos_venta = models.ManyToManyField(TipoVenta, related_name='productores')
    ferias_mercadillos = models.ManyToManyField(FeriaMercadillo, related_name='productores')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    last_login = models.DateTimeField(auto_now_add=True, null=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username','dni_prod', 'id_regepa']

    objects = ProductorManager()

    def __str__(self):
        return self.id_regepa

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True
    @property
    def direcciones_prod(self):
        direcciones_prod = TipoVenta.objects.get(tipo_venta="Venta de proximidad")
        return self.direccionesprod_set.filter(tipo_venta=direcciones_prod)
    
    @property
    def tiendas_prod(self):
        tiendas_prod = TipoVenta.objects.get(tipo_venta="Venta en establecimientos locales")
        return self.direccionesprod_set.filter(tipo_venta=tiendas_prod)

    @property
    def link_webs_prod(self):
        return self.productorurl_set.all()
    
    @property
    def mercadillo_prod(self):
        return self.ferias_mercadillos.all()


class DireccionesProd(models.Model):
    productor = models.ForeignKey(Productor, on_delete=models.CASCADE)
    calle = models.CharField(max_length=200)
    numero = models.CharField(max_length=10, null=True, blank=True)
    codigo_postal = models.CharField(max_length=10)
    provincia = models.ForeignKey(Provincia, on_delete=models.CASCADE)
    tipo_venta = models.ForeignKey(TipoVenta, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.calle}, {self.numero}, {self.codigo_postal}, {self.provincia}"

class ProductorURL(models.Model):
    productor = models.ForeignKey(Productor, on_delete=models.CASCADE)
    url = models.URLField()

    def __str__(self):
        return self.url
    
class EncuestaComunicacion(models.Model):
    productor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    frecuencia_uso = models.CharField(max_length=1)
    utilidad = models.CharField(max_length=1)
    eficacia = models.CharField(max_length=1)
    negocios = models.CharField(max_length=1)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Encuesta Comunicación {self.pk} - Productor {self.productor.id_regepa}"
    
    def get_fields(self):
        return [
            ('Fecha de creación', self.fecha_creacion),
            ('Frecuencia de uso', self.frecuencia_uso),
            ('Utilidad', self.utilidad),
            ('Eficacia', self.eficacia),
            ('Negocios', self.negocios),
        ]
    
class EncuestaRegistroVentaDirecta(models.Model):
    productor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    registro = models.CharField(max_length=1)
    informacion = models.CharField(max_length=1)
    facilidad = models.CharField(max_length=1)
    recomendacion = models.CharField(max_length=1)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Encuesta Registro Venta Directa {self.pk} - Productor {self.productor.id_regepa}"
    
    def get_fields(self):
        return [
            ('Fecha de creación', self.fecha_creacion),
            ('Registro', self.registro),
            ('Informacion', self.informacion),
            ('Facilidad', self.facilidad),
            ('Recomendacion', self.recomendacion),
        ]
    
class EncuestaMercadillos(models.Model):
    productor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    uso = models.CharField(max_length=1)
    utilidad = models.CharField(max_length=1)
    accesibilidad = models.CharField(max_length=1)
    participacion = models.CharField(max_length=1)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Encuesta Mercadillos {self.pk} - Productor {self.productor.id_regepa}"
    
    def get_fields(self):
        return [
            ('Fecha de creación', self.fecha_creacion),
            ('Uso', self.uso),
            ('Utilidad', self.utilidad),
            ('Accesibilidad', self.accesibilidad),
            ('Participacion', self.participacion),
        ]