# Seguridad y Control de Acceso con Django

Ejercicio de implementación manual de autenticación (Login/Logout) y autorización con permisos en Django.

## Requisitos

- Python 3.10+
- pip

## Instalación

```bash
# 1. Clonar e ingresar al proyecto
cd seguridad_acceso_django

# 2. Crear y activar entorno virtual
python3 -m venv venv
source venv/bin/activate

# 3. Instalar dependencias
pip install django

# 4. Ejecutar migraciones
python manage.py migrate

# 5. (Opcional) Poblar datos demo
python manage.py setup_groups

# 6. Iniciar servidor
python manage.py runserver
```

## Usuarios predefinidos

| Usuario     | Contraseña | Grupo       | Permisos                        |
|-------------|------------|-------------|---------------------------------|
| `admin`     | admin123   | superusuario| Todos                           |
| `demo_user` | demo1234   | Viewers     | `auth.view_user`                |

*(Correr `python manage.py setup_groups` para crearlos)*

## Arquitectura del proyecto

```
seguridad_acceso_django/
├── config/                  # Configuración del proyecto
│   ├── settings.py          # Apps, templates, LOGIN_URL, etc.
│   └── urls.py              # Enrutador raíz (incluye core.urls)
├── core/                    # App principal
│   ├── views.py             # Vistas de autenticación y autorización
│   ├── urls.py              # Rutas de la app
│   └── management/
│       └── commands/
│           └── setup_groups.py  # Comando para crear grupos y usuarios demo
├── templates/               # Plantillas HTML
│   ├── base.html            # Layout con Bootstrap 5
│   ├── home.html            # Página de inicio
│   ├── login.html           # Formulario de inicio de sesión
│   ├── register.html        # Formulario de registro
│   ├── dashboard.html       # Panel protegido (LoginRequiredMixin)
│   ├── profile.html         # Perfil protegido (LoginRequiredMixin)
│   ├── admin_users.html     # Lista de usuarios (permiso requerido)
│   ├── moderate.html        # Panel de moderación (permiso requerido)
│   └── 403.html             # Página de acceso denegado
└── manage.py
```

## Rutas disponibles

| Ruta             | Vista                          | Protección                          |
|------------------|--------------------------------|-------------------------------------|
| `/`              | `home`                         | Pública                             |
| `/register/`     | `RegisterView`                 | Pública (redirige si autenticado)   |
| `/login/`        | `LoginView`                    | Pública (redirige si autenticado)   |
| `/logout/`       | `LogoutView`                   | Pública                             |
| `/dashboard/`    | `DashboardView`                | `LoginRequiredMixin`                |
| `/profile/`      | `ProfileView`                  | `LoginRequiredMixin`                |
| `/admin-users/`  | `admin_users` (FBV)            | `@login_required + @permission_required('auth.view_user')` |
| `/moderate/`     | `ModerateContent` (CBV)        | `LoginRequiredMixin + PermissionRequiredMixin(perm='auth.change_user')` |

## Conceptos cubiertos

### 1. Login manual (sin vistas genéricas de Django)

`core/views.py:44` — `LoginView` usa `authenticate()` + `login()` de Django. Redirige autenticados al dashboard y maneja `?next=` para redirigir a la página original post-login.

### 2. Logout manual

`core/views.py:67` — `LogoutView` llama a `logout()` y redirige al login.

### 3. Registro de usuarios

`core/views.py:26` — `RegisterView` usa `UserCreationForm` customizado con Bootstrap y redirige al login tras el registro exitoso.

### 4. LoginRequiredMixin

`core/views.py:74,85,100` — `DashboardView`, `ProfileView` y `ModerateContent` heredan de `LoginRequiredMixin`. Si el usuario no está autenticado, Django redirige automáticamente a `LOGIN_URL = '/login/'`.

### 5. PermissionRequiredMixin

`core/views.py:100` — `ModerateContent` requiere el permiso `auth.change_user`. Si el usuario no tiene permiso pero está autenticado, muestra `403.html`.

### 6. @permission_required (FBV)

`core/views.py:92` — La vista `admin_users` usa el decorador `@permission_required('auth.view_user', raise_exception=True)`, lanzando un 403 si no se tiene el permiso.

### 7. Redirección post-login

`core/views.py:59` — Si se accede a una página protegida (ej. `/dashboard/`) sin sesión, Django redirige a `/login/?next=/dashboard/`. Al iniciar sesión, el usuario es redirigido automáticamente a la URL original. Probarlo: visitar `/dashboard/` sin estar logueado.

### 8. Página 403 personalizada

`core/views.py:104-106` — `ModerateContent.handle_no_permission()` renderiza `templates/403.html` cuando un usuario autenticado no tiene permisos.

### 9. Grupos y permisos

Ejecutar `python manage.py setup_groups` para crear:
- **Viewers** — `auth.view_user`
- **Moderators** — `auth.view_user` + `auth.change_user`

Los permisos se asignan desde las tablas del modelo `auth` de Django (`auth_permission`, `auth_group`, `auth_group_permissions`).

## Prueba rápida

```bash
# Iniciar servidor
source venv/bin/activate
python manage.py runserver

# En el navegador:
# - http://127.0.0.1:8000/              → Home
# - http://127.0.0.1:8000/register/      → Crear cuenta
# - http://127.0.0.1:8000/login/         → Iniciar sesión  
# - http://127.0.0.1:8000/dashboard/     → Dashboard (protegido)
# - http://127.0.0.1:8000/profile/       → Perfil (protegido)
# - http://127.0.0.1:8000/admin-users/   → Solo con permiso auth.view_user
# - http://127.0.0.1:8000/moderate/      → Solo con permiso auth.change_user
```

### Escenarios para probar permisos

1. **Login como `demo_user` (demo1234):** dashboard y perfil funcionan; `/admin-users/` funciona (tiene `view_user`); `/moderate/` da 403 (no tiene `change_user`).
2. **Login como `admin` (admin123):** todas las rutas funcionan.
3. **Sin sesión:** intentar `/dashboard/` → redirige a `/login/?next=/dashboard/`.
