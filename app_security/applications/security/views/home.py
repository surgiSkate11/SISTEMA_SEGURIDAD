from django.views.generic import TemplateView
from applications.security.components.menu_module import MenuModule
from applications.security.components.mixin_crud import PermissionMixin

class ModuloTemplateView(PermissionMixin,TemplateView):
    template_name = 'home.html'
   
    def get_context_data(self, **kwargs):
        context={}
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
        return context