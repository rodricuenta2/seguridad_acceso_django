================================================================================
 PROYECTO: SEGURIDAD Y CONTROL DE ACCESO CON DJANGO - ADMINISTRACION DE USUARIOS
================================================================================

1. DESCRIPCION
-------------------------------------------------------------------------------
Este proyecto implementa un sistema de autenticacion y autorizacion en Django
utilizando el modulo de administracion integrado de Django (django.contrib.admin).
El sitio administrativo permite gestionar usuarios, grupos y permisos de forma
grafica e intuitiva.

2. MODULO DE ADMINISTRACION DE DJANGO
-------------------------------------------------------------------------------
Django incluye un sitio administrativo preconstruido que se activa agregando
'django.contrib.admin' en INSTALLED_APPS. Este modulo proporciona interfaces
CRUD (Crear, Leer, Actualizar, Eliminar) para todos los modelos registrados.

El proyecto ya tiene configurado el admin en:
  - config/settings.py: contiene 'django.contrib.admin' en INSTALLED_APPS
  - config/urls.py: incluye path("admin/", admin.site.urls)

3. SUPERUSUARIO (ADMINISTRADOR)
-------------------------------------------------------------------------------
Se creo un superusuario con todos los privilegios para acceder al sitio admin:

  Usuario: admin
  Password: admin123
  Email: (vacio)

El superusuario tiene permisos totales sobre todos los modelos del sistema,
incluyendo la capacidad de crear, modificar y eliminar usuarios, grupos y
asignar permisos.

Comando utilizado:
  python manage.py createsuperuser

4. GESTION DE GRUPOS DE USUARIO
-------------------------------------------------------------------------------
Desde el sitio administrativo (http://127.0.0.1:8000/admin/auth/group/) se
pueden realizar las siguientes operaciones sobre grupos:

  - Crear nuevos grupos con nombre personalizado
  - Asignar permisos disponibles a cada grupo
  - Editar grupos existentes para agregar o quitar permisos
  - Eliminar grupos

Grupos predefinidos (creados via comando setup_groups):
  - Viewers: Permiso "auth | user | Can view user"
  - Moderators: Permisos "auth | user | Can view user"
                          "auth | user | Can change user"

5. GESTION DE USUARIOS
-------------------------------------------------------------------------------
Desde el sitio administrativo (http://127.0.0.1:8000/admin/auth/user/) se
pueden realizar las siguientes operaciones sobre usuarios:

  - Crear nuevos usuarios (username, password)
  - Editar datos personales (email, nombre, apellido)
  - Asignar grupos a los usuarios
  - Asignar permisos individuales (user permissions)
  - Definir estado del usuario:
      * Activo: puede iniciar sesion
      * Staff: puede acceder al sitio admin
      * Superusuario: tiene todos los permisos sin restricciones
  - Eliminar usuarios

Usuarios predefinidos:
  - admin (superuser / staff): Todos los permisos
  - demo_user (Viewers): Solo puede ver usuarios (auth.view_user)

6. GESTION DE PERMISOS
-------------------------------------------------------------------------------
Django utiliza un sistema de permisos basado en modelos (cada modelo genera
automaticamente permisos "add", "change", "delete", "view"). Desde el admin
se puede navegar y gestionar todos los permisos disponibles en el sistema en
(http://127.0.0.1:8000/admin/auth/permission/).

Los permisos se asignan a los usuarios de dos formas:
  a) Directamente: en la seccion "User permissions" del formulario de usuario
  b) Por grupo: agregando el usuario a un grupo que tenga los permisos

7. ARQUITECTURA DEL PROYECTO
-------------------------------------------------------------------------------
seguridad_acceso_django/
  +-- config/
  |   +-- settings.py          Configuracion del proyecto
  |   +-- urls.py              Ruta raiz (incluye admin y core.urls)
  |   +-- wsgi.py              WSGI config
  |   +-- asgi.py              ASGI config
  +-- core/
  |   +-- views.py             Vistas personalizadas (login, register, etc.)
  |   +-- urls.py              Rutas de la aplicacion core
  |   +-- admin.py             Registro de modelos en el admin
  |   +-- models.py            Modelos de datos
  |   +-- management/
  |       +-- commands/
  |           +-- setup_groups.py  Comando para crear grupos demo
  +-- templates/               Plantillas HTML con Bootstrap 5
  |   +-- base.html
  |   +-- login.html
  |   +-- register.html
  |   +-- dashboard.html
  |   +-- profile.html
  |   +-- admin_users.html
  |   +-- moderate.html
  |   +-- 403.html
  +-- manage.py                Script de gestion de Django
  +-- db.sqlite3               Base de datos SQLite
  +-- README.TXT               Este archivo

8. INSTRUCCIONES DE EJECUCION
-------------------------------------------------------------------------------
Requisitos:
  - Python 3.10+
  - pip

Pasos:

  1. Activar el entorno virtual:
     source venv/bin/activate

  2. Verificar que las migraciones esten aplicadas:
     python manage.py migrate

  3. (Opcional) Poblar grupos y usuarios demo:
     python manage.py setup_groups

  4. Iniciar el servidor de desarrollo:
     python manage.py runserver

  5. Acceder al sitio administrativo:
     http://127.0.0.1:8000/admin/
     Usuario: admin
     Password: admin123

  6. Explorar las secciones de gestion:
     - /admin/auth/user/     -> Gestion de usuarios
     - /admin/auth/group/    -> Gestion de grupos
     - /admin/auth/permission/ -> Gestion de permisos

9. RUTAS PUBLICAS DEL SITIO
-------------------------------------------------------------------------------
  /               Home (publico)
  /register/      Registro de nuevos usuarios (publico)
  /login/         Inicio de sesion (publico)
  /logout/        Cerrar sesion (publico)
  /dashboard/     Panel de control (requiere autenticacion)
  /profile/       Perfil de usuario (requiere autenticacion)
  /admin-users/   Lista de usuarios (requiere permiso auth.view_user)
  /moderate/      Panel de moderacion (requiere permiso auth.change_user)
  /admin/         Sitio administrativo de Django (requiere staff)

10. COMANDOS UTILES
-------------------------------------------------------------------------------
  python manage.py createsuperuser    Crear nuevo superusuario
  python manage.py setup_groups       Crear grupos y usuarios demo
  python manage.py migrate            Aplicar migraciones
  python manage.py runserver          Iniciar servidor
  python manage.py shell              Consola interactiva de Django

================================================================================
