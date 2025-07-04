from django.views.generic import TemplateView
from applications.security.models import Menu  # Ajusta si tu modelo está en otro lugar
from applications.security.components.menu_module import MenuModule

class SeguridadView(TemplateView):
    template_name = 'seguridad.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        MenuModule(self.request).fill(context)
        group = context.get('group')
        context['selected_group'] = group.name if group else None
        if not (self.request.user.is_superuser or (group and group.name == "Administrador")):
            context['menu_list'] = []
            context['title'] = 'Acceso denegado'
            context['access_denied'] = True
            return context
        # Buscar el menú llamado 'Seguridad' en el contexto generado
        menu = None
        for m in context.get('menu_list', []):
            if m['menu'].name.lower() == 'seguridad':
                menu = m
                break
        # Solo mostrar el menú Seguridad en el contenido principal, pero NO tocar sidebar_menu
        context['menu_list'] = [menu] if menu else []
        context['title'] = 'Seguridad'
        return context