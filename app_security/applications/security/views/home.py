from django.views.generic import TemplateView
from applications.security.components.menu_module import MenuModule
from applications.security.components.mixin_crud import PermissionMixin
from applications.core.models import Paciente
from datetime import date

class ModuloTemplateView(PermissionMixin,TemplateView):
    template_name = 'home.html'
   
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"]= "IC - Modulos"
        context["title1"]= "Modulos Disponibles"
        MenuModule(self.request).fill(context)
        # Extraer los menús "Herramientas" y "Sidebar" si existen
        herramientas_menu = None
        sidebar_menu = None
        for menu_item in context.get('menu_list', []):
            menu_name = getattr(menu_item['menu'], 'name', '').lower()
            if menu_name == 'herramientas':
                herramientas_menu = menu_item
            if menu_name == 'sidebar':
                sidebar_menu = menu_item
        context['herramientas_menu'] = herramientas_menu
        context['sidebar_menu'] = sidebar_menu

        # Calcular estadísticas de pacientes
        adultos = Paciente.objects.filter(activo=True, fecha_nacimiento__isnull=False).filter(
            fecha_nacimiento__lte=date.today().replace(year=date.today().year-18),
            fecha_nacimiento__gt=date.today().replace(year=date.today().year-60)
        ).count()
        ninos = Paciente.objects.filter(activo=True, fecha_nacimiento__isnull=False).filter(
            fecha_nacimiento__gt=date.today().replace(year=date.today().year-18)
        ).count()
        mayores = Paciente.objects.filter(activo=True, fecha_nacimiento__isnull=False).filter(
            fecha_nacimiento__lte=date.today().replace(year=date.today().year-60)
        ).count()
        context['pacientes_adultos'] = adultos
        context['pacientes_ninos'] = ninos
        context['pacientes_mayores'] = mayores
        return context