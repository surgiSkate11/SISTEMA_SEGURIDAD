def poblar_menus_modulos_permisos():
    from applications.security.models import Menu, Module, GroupModulePermission
    from django.contrib.auth.models import Group, Permission
    from django.contrib.contenttypes.models import ContentType

    # 1. Crear Menús principales
    menus_data = [
        {"name": "Pacientes",     "icon": "bi bi-people-fill",       "order": 1},
        {"name": "Citas",         "icon": "bi bi-calendar-event",    "order": 2},
        {"name": "Consultas",     "icon": "bi bi-clipboard-heart",   "order": 3},
        {"name": "Farmacia",      "icon": "bi bi-capsule",           "order": 4},
        {"name": "Reportes",      "icon": "bi bi-bar-chart",         "order": 5},
        {"name": "Usuarios",      "icon": "bi bi-person-badge",      "order": 6},
    ]
    menus_obj = []
    for m in menus_data:
        menu, created = Menu.objects.get_or_create(name=m["name"], defaults=m)
        menus_obj.append(menu)
    print("==== MENÚS CREADOS ====")
    for m in menus_obj:
        print(f"- {m.name}")

    # 2. Crear Módulos por menú (ejemplo)
    modulos_data = [
        # Pacientes
        {"name": "Listado de Pacientes", "menu": "Pacientes", "url": "/pacientes/", "order": 1},
        {"name": "Nuevo Paciente", "menu": "Pacientes", "url": "/pacientes/nuevo/", "order": 2},
        # Citas
        {"name": "Listado de Citas", "menu": "Citas", "url": "/citas/", "order": 1},
        {"name": "Nueva Cita", "menu": "Citas", "url": "/citas/nueva/", "order": 2},
        # ...agrega más módulos según tu estructura...
    ]
    modulos_obj = []
    for mod in modulos_data:
        menu = Menu.objects.get(name=mod["menu"])
        modulo, created = Module.objects.get_or_create(
            name=mod["name"],
            menu=menu,
            defaults={"url": mod["url"], "order": mod["order"]}
        )
        modulos_obj.append(modulo)
    print("==== MÓDULOS CREADOS ====")
    for m in modulos_obj:
        print(f"- {m.name} ({m.menu.name})")

    # 3. Crear Grupos y asignar permisos (ejemplo)
    grupos = ["Administradores", "Médicos", "Recepcionistas"]
    for g in grupos:
        group, created = Group.objects.get_or_create(name=g)
        print(f"Grupo: {group.name}")

    # 4. Asignar módulos a grupos (ejemplo)
    # Aquí puedes crear instancias de GroupModulePermission según tu modelo
    # Ejemplo:
    # for group in Group.objects.all():
    #     for modulo in Module.objects.all():
    #         GroupModulePermission.objects.get_or_create(group=group, module=modulo, defaults={"can_view": True})

    print("==== DATOS DE MENÚS, MÓDULOS Y GRUPOS CREADOS ====")

# Para ejecutar desde shell_plus:
# from applications.security.practices.orm_data2 import poblar_menus_modulos_permisos
# poblar_menus_modulos_permisos()