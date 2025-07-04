from django.contrib.auth.models import Group

def selected_group(request):
    group = None
    group_id = request.GET.get('gpid')
    if group_id:
        try:
            group = Group.objects.get(id=group_id)
        except Group.DoesNotExist:
            group = None
    # Si usas sesión para guardar el grupo seleccionado, puedes agregar aquí
    return {'selected_group': group.name if group else None}
