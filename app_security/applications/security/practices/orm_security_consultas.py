"""
Consultas ORM de ejemplo sobre los datos de seguridad del sistema médico.
Ejecución recomendada: python manage.py shell_plus < orm_security_consultas.py
"""

import os

def pausar_y_limpiar():
    input("Presione una tecla para continuar...")
    os.system('cls' if os.name == 'nt' else 'clear')

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from security.models import Menu, Module, GroupModulePermission

# ===============================
# 1. Listar todos los menús y sus módulos
# ===============================
# ORM shell_plus:
# for menu in Menu.objects.all(): print(menu.name, [m.name for m in menu.modules.all()])
print("==== MENÚS Y SUS MÓDULOS ====")
for menu in Menu.objects.all():
    print(f"{menu.name}:")
    for modulo in menu.modules.all():
        print(f"   - {modulo.name} ({modulo.url})")
pausar_y_limpiar()

# ===============================
# 2. Listar todos los grupos y los módulos donde tienen permisos
# ===============================
# ORM shell_plus:
# for grupo in Group.objects.all(): print(grupo.name, [gmp.module.name for gmp in grupo.module_permissions.all()])
print("==== GRUPOS Y SUS MÓDULOS CON PERMISOS ====")
for grupo in Group.objects.all():
    print(f"{grupo.name}:")
    for gmp in grupo.module_permissions.all():
        print(f"   - {gmp.module.name}")
pausar_y_limpiar()

# ===============================
# 3. Consultar qué permisos tiene cada grupo sobre cada módulo
# ===============================
# ORM shell_plus:
# for gmp in GroupModulePermission.objects.all(): print(gmp.group.name, gmp.module.name, [p.codename for p in gmp.permissions.all()])
print("==== PERMISOS DE CADA GRUPO POR MÓDULO ====")
for gmp in GroupModulePermission.objects.select_related('group', 'module').all():
    permisos = ', '.join([p.codename for p in gmp.permissions.all()])
    print(f"{gmp.group.name} → {gmp.module.name}: {permisos}")
pausar_y_limpiar()

# ===============================
# 4. Listar todos los usuarios con su(s) grupo(s)
# ===============================
# ORM shell_plus:
# User = get_user_model(); [(u.username, [g.name for g in u.groups.all()]) for u in User.objects.all()]
User = get_user_model()
print("==== USUARIOS Y SUS GRUPOS ====")
for u in User.objects.all():
    grupos = ', '.join([g.name for g in u.groups.all()])
    print(f"{u.username} ({u.email}) → {grupos if grupos else 'Sin grupo'}")
pausar_y_limpiar()

# ===============================
# 5. Consultar los permisos de un usuario según su(s) grupo(s) y módulo elegido
# ===============================
# ORM shell_plus:
# user = User.objects.get(username='medico1')
# grupo = user.groups.first()
# for gmp in grupo.module_permissions.all(): print(gmp.module.name, [perm.codename for perm in gmp.permissions.all()])
usuario_username = "medico1"
user = User.objects.get(username=usuario_username)
print(f"==== PERMISOS DE {usuario_username.upper()} POR MÓDULO ====")
for grupo in user.groups.all():
    print(f"Grupo: {grupo.name}")
    for gmp in grupo.module_permissions.all():
        permisos = ', '.join([perm.codename for perm in gmp.permissions.all()])
        print(f"   - {gmp.module.name}: {permisos}")
pausar_y_limpiar()

# ===============================
# 6. Consultar todos los permisos asignados a un módulo específico
# ===============================
# ORM shell_plus:
# modulo = Module.objects.get(name="Gestión de Pacientes")
# [perm.codename for perm in modulo.permissions.all()]
modulo_nombre = "Gestión de Pacientes"
modulo = Module.objects.get(name=modulo_nombre)
print(f"==== TODOS LOS PERMISOS DEL MÓDULO: {modulo_nombre} ====")
for perm in modulo.permissions.all():
    print(f"- {perm.codename}: {perm.name}")
pausar_y_limpiar()

# ===============================
# 7. Consultar qué usuarios pueden "agregar" pacientes (add_gestion_de_pacientes)
# ===============================
# ORM shell_plus:
# Permission.objects.get(codename='add_gestion_de_pacientes').groupmodulepermission_set.all()
permiso_codename = "add_gestion_de_pacientes"
permiso = Permission.objects.get(codename=permiso_codename)
print(f"==== USUARIOS CON PERMISO: {permiso_codename} ====")
for gmp in permiso.groupmodulepermission_set.all():
    grupo = gmp.group
    users = grupo.user_set.all()
    for user in users:
        print(f"{user.username} ({grupo.name})")
pausar_y_limpiar()

print("Consultas demostrativas finalizadas.")