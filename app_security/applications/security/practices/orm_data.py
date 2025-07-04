import os
from django.contrib.auth.models import Group
from applications.security.models import Menu, Module, User, GroupModulePermission

def pausar_y_limpiar():
    input("Presione una tecla para continuar...")
    os.system('cls' if os.name == 'nt' else 'clear')

# --- ELIMINAR TODO LO ANTERIOR ---
print("Eliminando datos previos...")
GroupModulePermission.objects.all().delete()
Module.objects.all().delete()
Menu.objects.all().delete()
Group.objects.all().delete()
User.objects.all().delete()
print("¡Datos previos eliminados!")
pausar_y_limpiar()

# --- 1. Crear MENÚS ---
print("Creando MENÚS...")
menus_data = [
    {"name": "Consultas", "icon": "bi bi-calendar-check", "order": 1},
    {"name": "Auditores", "icon": "bi bi-person-badge", "order": 2},
    {"name": "Emergencia", "icon": "bi bi-clipboard-pulse", "order": 3},
    {"name": "Registros", "icon": "bi bi-journal-medical", "order": 4},
    {"name": "Module", "icon": "bi bi-boxes", "order": 99},
    {"name": "Menu", "icon": "bi bi-list-columns", "order": 100},
]
menu_objs = {}
for data in menus_data:
    menu = Menu.objects.create(
        name=data["name"],
        icon=data["icon"],
        order=data["order"]
    )
    menu_objs[data["name"]] = menu
    print(f"Creado menú: {menu.name}")
pausar_y_limpiar()

# --- 2. Crear MÓDULOS ---
print("Creando MÓDULOS...")
modules_data = [
    # Consultas
    {"name": "Citas", "url": "citas/", "menu": "Consultas", "description": "Gestión de citas", "icon": "bi bi-calendar-event", "is_active": True, "order": 1},
    {"name": "Diagnósticos", "url": "diagnosticos/", "menu": "Consultas", "description": "Gestión de diagnósticos", "icon": "bi bi-clipboard2-pulse", "is_active": True, "order": 2},
    {"name": "Recetas", "url": "recetas/", "menu": "Consultas", "description": "Gestión de recetas", "icon": "bi bi-file-earmark-medical", "is_active": True, "order": 3},
    # Auditores
    {"name": "Usuarios", "url": "usuarios/", "menu": "Auditores", "description": "Gestión de usuarios", "icon": "bi bi-people", "is_active": True, "order": 1},
    {"name": "Configuración", "url": "configuracion/", "menu": "Auditores", "description": "Configuración del sistema", "icon": "bi bi-gear", "is_active": True, "order": 2},
    {"name": "Reportes", "url": "reportes/", "menu": "Auditores", "description": "Reportes y estadísticas", "icon": "bi bi-bar-chart", "is_active": True, "order": 3},
    # Emergencia
    {"name": "Registro de Pacientes", "url": "pacientes/", "menu": "Emergencia", "description": "Registro de pacientes", "icon": "bi bi-person-plus", "is_active": True, "order": 1},
    {"name": "Historial Médico", "url": "historial/", "menu": "Emergencia", "description": "Historial médico de pacientes", "icon": "bi bi-journal-medical", "is_active": True, "order": 2},
    {"name": "Seguimiento", "url": "seguimiento/", "menu": "Emergencia", "description": "Seguimiento de pacientes", "icon": "bi bi-activity", "is_active": True, "order": 3},
    # Administración
    {"name": "Módulo_Seguridad", "url": "security/module_list/", "menu": "MODULOS", "description": "Administrar módulos", "icon": "bi bi-boxes", "is_active": True, "order": 1},
    {"name": "Menú_Seguridad", "url": "security/menu_list/", "menu": "MENUS", "description": "Administrar menús", "icon": "bi bi-list-columns", "is_active": True, "order": 1},
]
module_objs = {}
for data in modules_data:
    module = Module.objects.create(
        name=data["name"],
        url=data["url"],
        menu=menu_objs[data["menu"]],
        description=data["description"],
        icon=data["icon"],
        is_active=data["is_active"],
        order=data["order"]
    )
    module_objs[data["name"]] = module
    print(f"Creado módulo: {module.name}")
pausar_y_limpiar()

# --- 3. Crear USUARIOS ---
print("Creando USUARIOS...")
users_data = [
    {"username": "drgomez2", "email": "drgomezz@clinica.med", "first_name": "Carlos", "last_name": "Gómez", "dni": "0912345678", "is_active": True, "password": "drgomez123", "is_superuser": False, "is_staff": False},
    {"username": "gabi", "email": "gabi@gmail.com", "first_name": "gabi", "last_name": "anda", "dni": "0967234567", "is_active": True, "password": "gabi123", "is_superuser": True, "is_staff": True},
]
user_objs = {}
for data in users_data:
    user = User.objects.create(
        username=data["username"],
        email=data["email"],
        first_name=data["first_name"],
        last_name=data["last_name"],
        dni=data["dni"],
        is_active=data["is_active"],
        is_superuser=data["is_superuser"],
        is_staff=data["is_staff"],
    )
    user.set_password(data["password"])
    user.save()
    user_objs[data["username"]] = user
    print(f"Creado usuario: {user.username}")
pausar_y_limpiar()

# --- 4. Crear GRUPOS ---
print("Creando GRUPOS...")
groups_data = [
    {"name": "Médicos"},
    {"name": "Asistentes"},
    {"name": "Superusuarios"},
]
group_objs = {}
for data in groups_data:
    group = Group.objects.create(name=data["name"])
    group_objs[data["name"]] = group
    print(f"Creado grupo: {group.name}")
pausar_y_limpiar()

# --- 5. Asignar USUARIOS a GRUPOS ---
print("Asignando USUARIOS a GRUPOS...")
user_objs["drgomez2"].groups.set([group_objs["Médicos"]])
user_objs["gabi"].groups.set([group_objs["Médicos"], group_objs["Asistentes"], group_objs["Superusuarios"]])
print("Usuarios asignados a grupos.")
pausar_y_limpiar()

# --- 6. Crear GroupModulePermission ---
print("Creando PERMISOS de grupo sobre módulos...")
gmp_data = [
    {"group": "Médicos", "module": "Diagnósticos"},
    {"group": "Médicos", "module": "Registro de Pacientes"},
    {"group": "Asistentes", "module": "Registro de Pacientes"},
    {"group": "Superusuarios", "module": "Módulo_Seguridad"},
    {"group": "Superusuarios", "module": "Menú_Seguridad"},
]
for data in gmp_data:
    gmp = GroupModulePermission.objects.create(
        group=group_objs[data["group"]],
        module=module_objs[data["module"]],
    )
    print(f"Creado permiso grupo-módulo: {data['group']} - {data['module']}")
pausar_y_limpiar()

# --- 7. Mostrar resumen ---
print("\nResumen de datos creados:")
print("Menús:")
for m in Menu.objects.all():
    print(f"- {m.id}: {m.name} ({m.icon})")
print("Módulos:")
for m in Module.objects.all():
    print(f"- {m.id}: {m.name} (Menu: {m.menu.name}, Icono: {m.icon})")
print("Usuarios:")
for u in User.objects.all():
    print(f"- {u.id}: {u.username} ({u.email}) Superuser: {u.is_superuser}")
print("Grupos:")
for g in Group.objects.all():
    print(f"- {g.id}: {g.name}")
print("Permisos Grupo-Módulo:")
for gmp in GroupModulePermission.objects.all():
    print(f"- Grupo: {gmp.group.name}, Módulo: {gmp.module.name}")

print("\n¡Carga de datos completada! Ahora puedes acceder correctamente al sistema.")
pausar_y_limpiar()