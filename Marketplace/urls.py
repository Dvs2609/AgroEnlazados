from django.urls import path
from . import views
from .views import HomePageView, CooperativaListView, ProductoresListView, ProductorDetailView, ProductorRegistrationView, CooperativaDetailView, ContactView  
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('', HomePageView.as_view(), name="home"),
    
    path('login/', views.iniciarSesion, name="login"),
    #path('registro/', views.registrarse, name="registro"),
    path('registro/', ProductorRegistrationView.as_view(), name='registro'),
    path('logout/', views.logoutUser, name="logout"),
    path('contacto/', ContactView.as_view(), name='contact'),

    path('<str:nombre>/cooperativas/', views.CooperativaListView.as_view(), name='cooperativas'),
    path('<str:nombre>/mercadillos/', views.FeriasMercadillosListView.as_view(), name='mercadillos'),
    path('<str:nombre>/productores/', views.ProductoresListView.as_view(), name='productores'),
    path('<str:nombre>/productores/<int:pk>/', ProductorDetailView.as_view(), name='perfil_productor'),
    
    path('productor/<int:pk>/actualizar_nombre_prod/', views.actualizar_nombre_prod, name='actualizar_nombre_prod'),
    path('productor/<int:pk>/actualizar_link_webs_prod/', views.actualizar_link_webs_prod, name='actualizar_link_webs_prod'),
    path('productor/<int:pk>/actualizar_productos_prod/', views.actualizar_productos_prod, name='actualizar_productos_prod'),
    path('productor/<int:pk>/actualizar_tiendas_prod/', views.actualizar_tiendas_prod, name='actualizar_tiendas_prod'),
    path('productor/<int:pk>/actualizar_direccion_prod/', views.actualizar_direccion_prod, name='actualizar_direccion_prod'),
    path('productor/<int:pk>/actualizar_telefono_prod/', views.actualizar_telefono_prod, name='actualizar_telefono_prod'),
    path('productor/<int:pk>/actualizar_tipos_venta/', views.actualizar_tipos_venta, name='actualizar_tipos_venta'),
    path('productor/<int:pk>/actualizar_ferias_mercadillos/', views.actualizar_ferias_mercadillos, name='actualizar_ferias_mercadillos'),
    path('productor/<int:pk>/actualizar_cp_prod/', views.actualizar_cp_prod, name='actualizar_cp_prod'),
    path('productor/<int:pk>/actualizar_email_prod/', views.actualizar_email_prod, name='actualizar_email_prod'),
    path('productor/<int:pk>/actualizar_id_regepa/', views.actualizar_id_regepa, name='actualizar_id_regepa'),

    path('productor/<int:pk>/anadir_producto/', views.add_producto_prod, name='add_producto_prod'),
    path('productor/<int:pk>/eliminar_producto/<int:producto_pk>/', views.eliminar_producto_prod, name='eliminar_producto_prod'),
    path('buscar_producto/', views.buscar_producto, name='buscar_producto'),

    #path('productor/<int:productor_pk>/add_direccion/', views.add_direccion, name='add_direccion'),
    path('productor/<int:productor_pk>/edit_direccion/<int:direccion_pk>/', views.edit_direccion, name='edit_direccion'),
    path('productor/<int:productor_pk>/add_direccion/', views.add_direccion, name='add_direccion'),
    path('productor/<int:productor_pk>/delete_direccion/', views.delete_direccion, name='delete_direccion'),
    #path('productor/<int:productor_id>/add_tienda/', views.add_tienda, name='add_tienda'),
    #path('productor/<int:productor_pk>/edit_tienda/<int:tienda_pk>/', views.edit_tienda, name='edit_tienda'),
    path('eliminar-mercadillo/<int:productor_id>/<int:mercadillo_id>/', views.eliminar_mercadillo, name='eliminar_mercadillo'),
    #path('productor/<int:pk>/anadir_tienda/', views.add_tienda_prod, name='add_tienda_prod'),
    #path('productor/<int:pk>/anadir_direccion/', views.add_direccion_prod, name='add_direccion_prod'),
    path('productor/<int:pk>/anadir_url/', views.anadir_url, name='anadir_url'),
    path('productor/<int:pk>/eliminar_url/', views.eliminar_url, name='eliminar_url'),
    
    path('<str:nombre>/ventas/', views.PaginaVentasView.as_view(), name='ventas'),

    path('<str:nombre>/ventas/<int:pk>/', views.TipoVentaView.as_view(), name='tipos_venta'),
    #path('filtrar_datos/', FiltrarDatosView.as_view(), name='filtrar_datos'),
    
    path('<str:nombre>/', views.paginaInicio, name='inicio'),
    path('cooperativa/<slug:slug>/', views.CooperativaDetailView.as_view(), name='cooperativa_detail'),

    #path('encuestas/enviar_correo_encuesta/', views.enviar_correo_encuesta, name='enviar_correo_encuesta'),
    path('encuestas/', views.encuestas, name='encuestas'),
    path('encuestas/comunicacion/', views.EncuestaComunicacionView.as_view(), name='encuesta_comunicacion'),
    path('encuestas/registro_venta_directa/', views.EncuestaRegistroVentaDirectaView.as_view(), name='encuesta_registro_venta_directa'),
    path('encuestas/satisfaccion_mercadillos/', views.EncuestaMercadillosView.as_view(), name='encuesta_mercadillos'),

    path('productor/<int:pk>/buscar_feria_mercadillo/', views.buscar_feria_mercadillo, name='buscar_feria_mercadillo'),
    path('productor/<int:pk>/anadir_feria_mercadillo/', views.anadir_feria_mercadillo, name='anadir_feria_mercadillo'),
]