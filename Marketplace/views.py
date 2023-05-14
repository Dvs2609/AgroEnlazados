from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from .funciones import *
from django.views.generic import DetailView
from Marketplace.models import Productor, TipoVenta, ComunidadAutonoma, Provincia, Producto, DireccionesProd, FeriaMercadillo, ProductorURL
from .models import Cooperativa
from .models import TipoVenta
from django.views.generic import ListView
from django.views.generic import TemplateView
from django.views.generic import View
import django_filters
from django_tables2 import Table, Column, LinkColumn, A
import django_tables2 as tables
from .forms import ProductorRegistrationForm
from .forms import LoginForm, FiltroIndex
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.views.generic.edit import FormView
from django.views.decorators.csrf import csrf_exempt
from django_filters import FilterSet, CharFilter
from django.views.generic import ListView
from .forms import EncuestaComunicacionForm, EncuestaRegistroVentaDirectaForm, EncuestaMercadillosForm
from .models import EncuestaComunicacion, EncuestaRegistroVentaDirecta, EncuestaMercadillos
from django.core.mail import send_mail
# Create your views here.

class HomePageView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['view_name'] = 'index'  # Add the view_name to the context
        return context

    def get(self, request, *args, **kwargs):
        form = FiltroIndex()
        context = self.get_context_data()
        context['form'] = form
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        form = FiltroIndex(request.POST)
        if form.is_valid():
            comunidad_autonoma = form.cleaned_data['comunidad_autonoma']
            provincia = form.cleaned_data['provincia']
            if provincia:
                nombre = provincia.provincia
            elif comunidad_autonoma:
                nombre = comunidad_autonoma.nombre
            else:
                return render(request, self.template_name, {'form': form})
            
            # Guarda la provincia en la sesión
            request.session['provincia'] = str(nombre)
            return redirect(f'/{nombre}/')
        context = {
            'view_name': 'index',
            'form': form,  
        } 
        return render(request, self.template_name, context)
        
def paginaInicio(request, nombre):
    context = {
        'nombre': nombre,
    }
    return render(request, 'inicio.html', context)    

class PaginaVentasView(ListView):
    model = TipoVenta
    template_name = 'ventas.html'
    context_object_name = 'ventas'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        nombre = self.kwargs['nombre']
        context['nombre'] = nombre
        context['provincia'] = nombre

        imagenes = [
            '../static/images/img-venta-tiendas.png',
            '../static/images/img-venta-cooperativa.jpg',
            '../static/images/img-venta-online.png',
            '../static/images/img-venta-abasto.jpg',
            '../static/images/img-venta-prox.webp',
        ]

        ventas_con_imagenes = []
        for index, venta in enumerate(context['ventas']):
            ventas_con_imagenes.append((venta, imagenes[index % len(imagenes)]))

        context['ventas_con_imagenes'] = ventas_con_imagenes

        return context

class TipoVentaView(DetailView):
    model = TipoVenta
    template_name = 'tipos_venta.html'
    context_object_name = 'venta'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        nombre = self.kwargs['nombre']
        context['nombre'] = nombre
        context['provincia'] = nombre
        return context


def tipos_venta(request, id_tipo_venta):
    venta = get_object_or_404(TipoVenta, pk=id_tipo_venta)
    return render(request, 'tipos_venta.html', {'venta': venta})

class CooperativaTable(Table):
    denominación_social = Column(attrs={"td": {"class": "coop-link", "data-slug": lambda record: record.slug, "data-lat": lambda record: record.latitude, "data-lon": lambda record: record.longitude}}, orderable=True, verbose_name='Denominación social', accessor='denominación_social')

    class Meta:
        model = Cooperativa
        fields = ('num_inscripcion', 'denominación_social', 'provincia_coop', 'localidad_coop', 'cp_coop', 'grado_coop', 'fecha_inscripcion_coop')
        template_name = 'django_tables2/bootstrap.html'

class CooperativaFilter(django_filters.FilterSet):
    denominación_social = django_filters.CharFilter(field_name='denominación_social', lookup_expr='icontains' , label='Filtro por nombre de cooperativa')
    provincia_coop = django_filters.CharFilter(field_name='provincia_coop__provincia', lookup_expr='icontains', label='Filtro por provincia') 
    localidad_coop = django_filters.CharFilter(field_name='localidad_coop', lookup_expr='icontains', label='Filtro por localidad')

    class Meta:
        model = Cooperativa
        fields = ['denominación_social', 'provincia_coop', 'localidad_coop']

class CooperativaListView(ListView):
    model = Cooperativa
    template_name = 'cooperativas.html'
    context_object_name = 'cooperativas'
    paginate_by = 6

    def get_queryset(self):
        nombre = self.kwargs['nombre']
        search = self.request.GET.get('search', '')
        provincia = Provincia.objects.filter(provincia=nombre).first()
        if provincia:
            queryset = Cooperativa.objects.filter(provincia_coop=provincia)
        else:
            comunidad_autonoma = ComunidadAutonoma.objects.filter(nombre=nombre).first()
            if comunidad_autonoma:
                queryset = Cooperativa.objects.filter(ccaa_coop=comunidad_autonoma)
            else:
                queryset = Cooperativa.objects.none()

        # Aplicar el filtro aquí
        cooperativa_filter = CooperativaFilter(self.request.GET, queryset=queryset)
        queryset = cooperativa_filter.qs

        if search:
            queryset = queryset.filter(denominación_social__icontains=search)

        # Aquí ordenamos el queryset por el campo denominación_social antes de retornarlo
        return queryset.order_by('denominación_social')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cooperativa_filter = CooperativaFilter(self.request.GET, queryset=self.object_list) # Cambia esto
        cooperativa_table = CooperativaTable(cooperativa_filter.qs)
        tables.RequestConfig(self.request, paginate={'per_page': self.paginate_by}).configure(cooperativa_table)
        context['filter'] = cooperativa_filter
        context['table'] = cooperativa_table
        return context
    
class CooperativaDetailView(DetailView):
    model = Cooperativa
    template_name = 'cooperativa_detail.html'
    context_object_name = 'cooperativa'
    slug_url_kwarg = 'slug'

def iniciarSesion(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            print("Logueado")
            request.session['provincia'] = user.provincia_prod.provincia
            return redirect('inicio', nombre=request.session['provincia'])          
        else:
            print("Error en el formulario")
            # Aquí puedes manejar el caso cuando las credenciales no son válidas
            pass
    context = {
        'view_name': 'login',
    }            
    return render(request, 'login.html', context)


class ProductorRegistrationView(FormView):
    template_name = 'register.html'
    form_class = ProductorRegistrationForm
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['provincias'] = Provincia.objects.all()
        context['comunidades'] = ComunidadAutonoma.objects.all()
        return context

    def form_valid(self, form):
        productor = form.save(commit=False)
        productor.ccaa_prod = ComunidadAutonoma.objects.get(id=self.request.POST['ccaa_prod'])
        productor.provincia_prod = Provincia.objects.get(id=self.request.POST['provincia_prod'])
        productor.save()
        form.save_m2m()
        # Iniciar sesión del usuario después del registro
        login(self.request, productor)

        # Almacenar la provincia en la sesión
        self.request.session['nombre'] = productor.provincia_prod.provincia

        # Redirigir al usuario a la página de inicio
        return redirect('inicio', nombre=self.request.session['nombre'])

def logoutUser(request):
    logout(request)
    return redirect('home')

class ProductoresTable(tables.Table):
    id_regepa = tables.Column(verbose_name='ID Regepa')
    nombre_prod = tables.Column(verbose_name='Nombre', linkify=lambda record: reverse('perfil_productor', args=[str(record.provincia_prod), str(record.pk)]))
    productos_prod = tables.Column(empty_values=(), verbose_name='Productos')    
    provincia_prod = tables.Column(verbose_name='Provincia')
    cp_prod = tables.Column(verbose_name='Código Postal')
    tipos_venta = tables.Column(empty_values=(), verbose_name='Tipos de venta', attrs={"td": {"class": "columna-tipos-venta"}})

    class Meta:
        model = Productor
        fields = ('id_regepa', 'nombre_prod', 'productos_prod', 'provincia_prod', 'cp_prod', 'tipos_venta')
        template_name = 'django_tables2/bootstrap.html'

    def render_tipos_venta(self, value):
        return format_html('<br>'.join([tv.tipo_venta for tv in value.all()]))

    def render_productos_prod(self, record):
        productos = record.productos_prod.all()
        return ', '.join([str(producto) for producto in productos])
        
    def render_tipos_venta(self, value):
        return ', '.join([tv.tipo_venta for tv in value.all()])
    
    
    
class ProductoresFilter(django_filters.FilterSet):
    id_regepa = django_filters.NumberFilter(field_name='id_regepa', lookup_expr='icontains', label='Filtro Id REGEPA')
    nombre_prod = django_filters.CharFilter(field_name='nombre_prod', lookup_expr='icontains', label='Filtro por nombre de productor')
    productos_prod = django_filters.CharFilter(field_name='productos_prod__nombre', lookup_expr='icontains', label='Filtro de productos')

    class Meta:
        model = Productor
        fields = ['id_regepa', 'nombre_prod', 'productos_prod']

class ProductoresListView(ListView):
    model = Productor
    ordering = ['nombre_prod']
    template_name = 'productores.html'
    context_object_name = 'productores'
    paginate_by = 6

    def get_queryset(self):
        nombre = self.kwargs['nombre']
        provincia = Provincia.objects.filter(provincia=nombre).first()
        if provincia:
            return Productor.objects.filter(provincia_prod=provincia).order_by('nombre_prod')
        comunidad_autonoma = ComunidadAutonoma.objects.filter(nombre=nombre).first()
        if comunidad_autonoma:
            return Productor.objects.filter(ccaa_prod=comunidad_autonoma).order_by('nombre_prod')
        return Productor.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        productores_filter = ProductoresFilter(self.request.GET, queryset=self.get_queryset())
        productores_table = ProductoresTable(productores_filter.qs)
        tables.RequestConfig(self.request, paginate={'per_page': self.paginate_by}).configure(productores_table)
        context['filter'] = productores_filter
        context['table'] = productores_table
        context['nombre'] = self.kwargs['nombre']
        # Añadir información de cooperativaMapa al contexto
        context['productoresMapa'] = Productor.objects.all()
        return context

from django.db.models import F
class ProductorDetailView(DetailView):
    model = Productor
    template_name = 'perfil_productores.html'
    
    def get_object(self, queryset=None):
        return Productor.objects.get(pk=self.kwargs['pk'])
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        productor = self.get_object()
        direcciones_unicas = productor.direccionesprod_set.values('tipo_venta', tipo_venta_name=F('tipo_venta__tipo_venta')).distinct()

        context['current_user'] = self.request.user
        context['add_form'] = AddDireccionForm()
        context['add_form2'] = EditDireccionForm()
        context['direcciones_unicas'] = direcciones_unicas

        # Añadir los formularios de encuestas al contexto
        context['encuesta_comunicacion_form'] = EncuestaComunicacionForm()
        context['encuesta_registro_venta_directa_form'] = EncuestaRegistroVentaDirectaForm()
        context['encuesta_mercadillos_form'] = EncuestaMercadillosForm()

        return context


def actualizar_nombre_prod(request, pk):
    productor = Productor.objects.get(pk=pk)

    if request.method == 'POST':
        new_value = request.POST.get('new_value')
        productor.nombre_prod = new_value
        productor.save()
        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'error'})


def actualizar_link_webs_prod(request, pk):
    if request.method == 'POST':
        new_value = request.POST.get('new_value')
        productor = Productor.objects.get(pk=pk)
        productor.link_webs_prod = new_value
        productor.save()
        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'error'})
    

def actualizar_productos_prod(request, pk):
    if request.method == 'POST':
        new_value = request.POST.get('new_value')
        productor = Productor.objects.get(pk=pk)
        productor.productos_prod = new_value
        productor.save()
        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'error'})
    

def actualizar_tiendas_prod(request, pk):
    if request.method == 'POST':
        new_value = request.POST.get('new_value')
        productor = Productor.objects.get(pk=pk)
        productor.tiendas_prod = new_value
        productor.save()
        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'error'})
    

def actualizar_direccion_prod(request, pk):
    if request.method == 'POST':
        new_value = request.POST.get('new_value')
        productor = Productor.objects.get(pk=pk)
        productor.dirección_prod = new_value
        productor.save()
        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'error'})

def actualizar_telefono_prod(request, pk):
    if request.method == 'POST':
        new_value = request.POST.get('new_value')
        productor = Productor.objects.get(pk=pk)
        productor.teléfono_prod = new_value
        productor.save()
        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'error'})

def actualizar_tipos_venta(request, pk):
    if request.method == 'POST':
        new_value = request.POST.get('new_value')
        productor = Productor.objects.get(pk=pk)
        productor.tipos_venta = new_value
        productor.save()
        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'error'})

def actualizar_ferias_mercadillos(request, pk):
    if request.method == 'POST':
        new_value = request.POST.get('new_value')
        productor = Productor.objects.get(pk=pk)
        productor.ferias_mercadillos = new_value
        productor.save()
        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'error'})
    
def actualizar_id_regepa(request, pk):
    if request.method == 'POST':
        new_value = request.POST.get('new_value')
        productor = Productor.objects.get(pk=pk)
        productor.id_regepa = new_value
        productor.save()
        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'error'})
    
def actualizar_cp_prod(request, pk):
    if request.method == 'POST':
        new_value = request.POST.get('new_value')
        productor = Productor.objects.get(pk=pk)
        productor.cp_prod = new_value
        productor.save()
        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'error'})    

def actualizar_email_prod(request, pk):
    if request.method == 'POST':
        new_value = request.POST.get('new_value')
        productor = Productor.objects.get(pk=pk)
        productor.email = new_value
        productor.save()
        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'error'})  
    
@csrf_exempt
def add_producto_prod(request, pk):
    if request.method == 'POST':
        productor = Productor.objects.get(pk=pk)
        producto_id = request.POST.get('id')
        if producto_id:
            producto = Producto.objects.get(id=producto_id)
            productor.productos_prod.add(producto)
            productor.save()
            return JsonResponse({'producto': {'nombre': producto.nombre}})
        else:
            return JsonResponse({'error': 'Id de producto no válido'})
    else:
        return JsonResponse({'status': 'error'})

from django.db.models import Q

def buscar_producto(request):
    query = request.GET.get('q', '')
    productos = Producto.objects.filter(Q(nombre__icontains=query))
    productos_json = [{'nombre': producto.nombre, 'id': producto.id} for producto in productos]
    return JsonResponse({'productos': productos_json})
 
@csrf_exempt
def eliminar_producto_prod(request, pk, producto_pk):
    if request.method == 'POST':
        productor = Productor.objects.get(pk=pk)
        if producto_pk:
            producto = Producto.objects.get(id=producto_pk)
            productor.productos_prod.remove(producto)
            productor.save()
            return JsonResponse({'status': 'ok'})
        else:
            return JsonResponse({'error': 'Id de producto no válido'})
    else:
        return JsonResponse({'status': 'error'})
import json
@csrf_exempt
def actualizar_direccion_prod(request, pk):
    if request.method == 'POST':
        data = json.loads(request.body)
        address = data.get('address')

        productor = Productor.objects.get(pk=pk)
        productor.direccion = address
        productor.save()

        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'error'})

class FeriasMercadillosTable(tables.Table):
    #nombre_fm = tables.Column(verbose_name='Nombre', linkify=lambda record: reverse('perfil_mercadillo', args=[str(record.localidad_fm), str(record.pk)]))

    class Meta:
        model = FeriaMercadillo
        fields = ('nombre_fm', 'días_fm', 'ubicación_fm', 'provincia_fm' , 'horario_fm', 'num_puestos_fm', 'tipo_fm')
        template_name = 'django_tables2/bootstrap.html'

class FeriasMercadillosFilter(django_filters.FilterSet):
    nombre_fm = django_filters.CharFilter(field_name='nombre_fm', lookup_expr='icontains', label='Filtro por nombre de mercadillo')
    provincia_fm = django_filters.CharFilter(field_name='provincia_fm__provincia', lookup_expr='icontains', label='Filtro por provincia')

    class Meta:
        model = FeriaMercadillo
        fields = ['nombre_fm', 'provincia_fm']
    
class FeriasMercadillosListView(ListView):
    model = FeriaMercadillo
    template_name = 'mercadillos.html'
    context_object_name = 'mercadillos'
    paginate_by = 6

    def get_queryset(self):
        nombre = self.kwargs['nombre']
        provincia = Provincia.objects.filter(provincia=nombre).first()
        if provincia:
            return FeriaMercadillo.objects.filter(provincia_fm=provincia).order_by('nombre_fm')
        comunidad_autonoma = ComunidadAutonoma.objects.filter(nombre=nombre).first()
        if comunidad_autonoma:
            return FeriaMercadillo.objects.filter(ccaa_fm=comunidad_autonoma).order_by('nombre_fm')
        return FeriaMercadillo.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ferias_mercadillos_filter = FeriasMercadillosFilter(self.request.GET, queryset=self.get_queryset())
        ferias_mercadillos_table = FeriasMercadillosTable(ferias_mercadillos_filter.qs)
        tables.RequestConfig(self.request, paginate={'per_page': self.paginate_by}).configure(ferias_mercadillos_table)
        context['filter'] = ferias_mercadillos_filter
        context['table'] = ferias_mercadillos_table
        context['nombre'] = self.kwargs['nombre']
        return context
    

class EncuestaComunicacionView(View):
    def post(self, request, *args, **kwargs):
        form = EncuestaComunicacionForm(request.POST)
        if form.is_valid():
            encuesta = EncuestaComunicacion(productor=request.user, **form.cleaned_data)
            encuesta.save()
            return JsonResponse({'result': 'success'})
        else:
            return JsonResponse({'result': 'error'})

class EncuestaRegistroVentaDirectaView(View):
    def post(self, request, *args, **kwargs):
        form = EncuestaRegistroVentaDirectaForm(request.POST)
        if form.is_valid():
            encuesta = EncuestaRegistroVentaDirecta(productor=request.user, **form.cleaned_data)
            encuesta.save()
            return JsonResponse({'result': 'success'})
        else:
            return JsonResponse({'result': 'error'})

class EncuestaMercadillosView(View):
    def post(self, request, *args, **kwargs):
        form = EncuestaMercadillosForm(request.POST)
        if form.is_valid():
            encuesta = EncuestaMercadillos(productor=request.user, **form.cleaned_data)
            encuesta.save()
            return JsonResponse({'result': 'success'})
        else:
            return JsonResponse({'result': 'error'})


def encuestas(request):
    return render(request, 'perfil_productores.html', {
        'encuesta_comunicacion_form': EncuestaComunicacionForm(),
        'encuesta_registro_venta_directa_form': EncuestaRegistroVentaDirectaForm(),
        'encuesta_mercadillos_form': EncuestaMercadillosForm(),
    })


"""from django.core.mail import send_mail
from django.template.loader import render_to_string

def enviar_correo_encuesta(encuesta, subject):
    message = render_to_string('correo_encuesta.html', {'encuesta': encuesta})
    from_email = 'dvs2609@gmail.com'
    recipient_list = ['d38df7490e64e7@inbox.mailtrap.com']  # Reemplazar con el correo electrónico del administrador
    send_mail(subject, message, from_email, recipient_list, fail_silently=False)"""


from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import DireccionesProd
from .forms import AddDireccionForm, EditDireccionForm
from django.template.loader import render_to_string
def add_direccion(request, productor_pk):
    if request.method == 'POST':
        form = AddDireccionForm(request.POST)
        if form.is_valid():
            direccion = form.save(commit=False)
            direccion.productor_id = productor_pk
            direccion.tipo_venta_id = request.POST.get('tipo_venta')  # obtener tipo_venta del cuerpo de la solicitud POST
            direccion.save()

            # Añadir TipoVenta al Productor
            productor = Productor.objects.get(pk=productor_pk)
            tipo_venta = request.POST.get('tipo_venta')
            productor.tipos_venta.add(tipo_venta)
            productor.save()

            return JsonResponse({'status': 'ok'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Error al agregar la dirección'})
    else:
        form = AddDireccionForm()
        form_html = render_to_string('direccion_form.html', {'form': form,}, request=request)
        return JsonResponse({'form_html': form_html})


def edit_direccion(request, productor_pk, direccion_pk):
    direccion = get_object_or_404(DireccionesProd, pk=direccion_pk)
    if request.method == 'POST':
        form = EditDireccionForm(request.POST, instance=direccion)
        if form.is_valid():
            updated_direccion = form.save(commit=False)
            updated_direccion.pk = direccion_pk
            updated_direccion.save()
            return JsonResponse({'status': 'ok'})
        else:
            return JsonResponse({'status': 'error'})
    else:
        form = EditDireccionForm(instance=direccion)
        form_html = render_to_string('direccion_form.html', {'form': form}, request=request)
        return JsonResponse({'form_html': form_html})


def delete_direccion(request, productor_pk):
    if request.method == 'POST':
        direccion_id = request.POST.get('direccion_id')
        try:
            direccion = DireccionesProd.objects.get(pk=direccion_id, productor_id=productor_pk)
            direccion.delete()
            return JsonResponse({'status': 'ok'})
        except DireccionesProd.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Direccion no encontrada'})

def buscar_feria_mercadillo(request, pk):
    query = request.GET.get('q', '')
    ferias_mercadillos = FeriaMercadillo.objects.filter(Q(nombre_fm__icontains=query))
    ferias_mercadillos_json = [{'nombre': feria_mercadillo.nombre_fm, 'id_fm': feria_mercadillo.id_fm} for feria_mercadillo in ferias_mercadillos]
    return JsonResponse({'ferias_mercadillos': ferias_mercadillos_json})


@csrf_exempt
def anadir_feria_mercadillo(request, pk):
    if request.method == 'POST':
        productor = Productor.objects.get(pk=pk)
        
        data = json.loads(request.body)
        feria_mercadillo_id = data.get('id_fm')
        
        if feria_mercadillo_id:
            feria_mercadillo = FeriaMercadillo.objects.get(id_fm=feria_mercadillo_id)
            productor.ferias_mercadillos.add(feria_mercadillo)
            tipo_venta = TipoVenta.objects.get(tipo_venta="Venta en ferias, mercadillos y de forma ambulante")  # Asegúrate de que este valor exista en tu base de datos
            productor.tipos_venta.add(tipo_venta)

            productor.save()
            return JsonResponse({'feria_mercadillo': {'nombre': feria_mercadillo.nombre_fm}})
        else:
            return JsonResponse({'error': 'Id de feria o mercadillo no válido'})
    else:
        return JsonResponse({'status': 'error'})

def eliminar_mercadillo(request, productor_id, mercadillo_id):
    productor = get_object_or_404(Productor, pk=productor_id)
    mercadillo = get_object_or_404(FeriaMercadillo, pk=mercadillo_id)

    productor.ferias_mercadillos.remove(mercadillo)

    return JsonResponse({'status': 'success'})

def anadir_url(request, pk):
    if request.method == "POST":
        productor = get_object_or_404(Productor, pk=pk)
        url = request.POST.get('url')

        if url:  # Verificar que el campo de URL no esté vacío
            productor_url = ProductorURL.objects.create(productor=productor, url=url)
            return JsonResponse({'status':'success'})
        else:
            return JsonResponse({'status':'error', 'error':'URL field is empty'})

    return JsonResponse({'status':'error', 'error':'Invalid request'})

def eliminar_url(request, pk):
    if request.method == "POST":
        data = json.loads(request.body)
        url_id = data.get('url_id')
        url = get_object_or_404(ProductorURL, pk=url_id)
        url.delete()

        return JsonResponse({'status':'success'})

    return JsonResponse({'status':'error', 'error':'Invalid request'})

class ContactView(View):
    def post(self, request, *args, **kwargs):
        issue_type = request.POST.get('issue_type')
        message = request.POST.get('message')

        if issue_type and message:
            send_mail(
                f'Mensaje de contacto - {issue_type}',
                message,
                '08129dbb0bcf9e@inbox.mailtrap.io',  # Remitente
                ['08129dbb0bcf9e@inbox.mailtrap.io'],  # Destinatario
            )
            messages.success(request, 'Tu mensaje ha sido enviado. Gracias por contactarnos.')
        else:
            messages.error(request, 'Por favor, completa todos los campos.')

        return redirect('home')