# AGROENLAZADOS

## Descripción del proyecto
Breve descripción del proyecto y su propósito.

## Manual de implementación
A continuación se describe como descargar e implementar el proyecto en un nuevo dispositivo.

## Manual de Usuario
A continuación se describe el funcionamiento y las características principales de AgroEnlazados.


### Elección de provincia/comunidad para entrar en AgroEnlazados
- Permite a los usuarios seleccionar su provincia o comunidad para acceder a información relevante según su ubicación.
    ![Elección de provincia/comunidad](UserManual_images/eleccion_provincia.png)

### Login
- Permite a los usuarios iniciar sesión si ya tienen una cuenta en AgroEnlazados
    ![Login](UserManual_images/login.png)

### Registro
- Permite a los nuevos usuarios crear una cuenta en AgroEnlazados. Necesitarán el identificador de REGEPA y el DNI para realizar el registro.
    ![Registro](UserManual_images/registro.png)

### Inicio y redirecciones de inicio
![Inicio](UserManual_images/inicio.png)
- Los usuarios son redirigidos a una página de inicio personalizada después de iniciar sesión, registrarse o haber elegido en la pagina inicial la provincia o cumunidad.
- En esta página se proporcionan enlaces rápidos a las siguientes secciones:
    - Cooperativas
    - Productores
    - Ventas
    - Mercadillos

### Tipos de venta
![Tipos de Venta](UserManual_images/tiposventa.png)
- AgroEnlazados ofrece diferentes tipos de ventas:   
    - Venta de Proximidad   
    - Venta en Ferias, Mercadillos y Mercados ambulantes  
    - Venta en Establecimientos y Tiendas locales
    - Venta en Cooperativas
    - Venta Online

### Tipos de venta
- Desde la pagina de tipos de venta pueden acceder a una página como esta con informacion sobre el tipo de venta:
    - Venta de Proximidad
    ![Venta de Proximidad](UserManual_images/Vproximidad.png)

    - Venta en Ferias, Mercadillos y Mercados ambulantes
    ![Venta en Mercadillos](UserManual_images/Vmercadillo.png)

### Navbar

- La barra de navegación (navbar) permite a los usuarios acceder fácilmente a diferentes secciones y funciones del sitio web.
    
    - Navbar pagina de eleccion de provincia, inicio y login
    ![Navbar0](UserManual_images/navbar0.png)
    
    - Navbar en las demas vistas
    ![Navbar1](UserManual_images/navbar1.png)
 
    - Navbar en las demas vistas con usuario logueado
    ![Navbar2](UserManual_images/navbar2.png)

### Filtros para tablas
![Filtros Cooperativa](UserManual_images/filtrocoop.png)
![Filtros Productor](UserManual_images/filtroprod.png)
![Filtros Mercadillos](UserManual_images/filtrofm.png)
- Los filtros de tabla permiten a los usuarios refinar sus búsquedas y encontrar información específica relacionada con productos agrícolas, cooperativas, productores, ventas, etc.

### Mapa
![Mapa](UserManual_images/mapa.png)
- El mapa proporciona una visualización geográfica de las cooperativas de Extremadura. El mapa muestra las cooperativas que aparezcan en ese momento en la tabla.

### Tabla y paginado
![Tabla Cooperativa](UserManual_images/tablacoop.png)
![Tabla Productor](UserManual_images/tablaprod.png)
![Tabla Mercadillos](UserManual_images/tablafm.png)
- Las secciones de productores, cooperativas y mercadillos se presentan en forma de tabla con paginación para facilitar la navegación y exploración de la información.

### Perfil del productor

- Sin iniciar sesión:
![Perfil del productor no logueado](UserManual_images/perfil_productorNL.png)
    - Los usuarios pueden ver la información del productor y contactarlo a través de correo electrónico y teléfono.

- Iniciado sesión:
![Perfil del productor logueado](UserManual_images/perfil_productorL.png)
    - Además de ver la información del productor, los usuarios pueden realizar las siguientes acciones en su propio perfil:
  
        - Editar nombre, identificación, correo electrónico, teléfono y código postal.
        ![Editar Info](UserManual_images/editname.png)

        - Añadir y eliminar productos.
        ![Añadir producto](UserManual_images/addprod.png)

        - Añadir dirección y tienda (Se diferencian en que cada modal tiene default el tipo de venta que realiza).
        ![Añadir dirección](UserManual_images/adddireccion.png)

        - Editar dirección y tienda. Para facilitar al usuario se insertan todos las variables de ese campo para que sea mas facil la edición.
        ![Editar dirección](UserManual_images/editdireccion.png)

        - Eliminar dirección y tienda.
         ![Eliminar dirección](UserManual_images/deletedireccion.png)

        - Añadir y eliminar ferias y mercadillos.
        ![Añadir mercadillo](UserManual_images/addfm.png)

        - Añadir links de webs.
        ![Añadir url](UserManual_images/addurl.png)

        - Ejemplo de encuestaa.
        ![Encuesta1](UserManual_images/encuesta.png)

### Footer
![Footer](UserManual_images/footer.png)
- Desde el pie de página el usuario podrá enviar un mensaje comentado sus quejas, sugerencias o reportes.
