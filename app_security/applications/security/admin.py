from django.contrib import admin

# security/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Menu, Module, GroupModulePermission

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'dni', 'is_staff')
    fieldsets = UserAdmin.fieldsets + (
        ('Información adicional', {'fields': ('dni', 'image', 'direction', 'phone')}),
    )

@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ('name', 'icon', 'order')
    search_fields = ('name',)
    ordering = ('order', 'name')

@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ('name', 'url', 'menu', 'is_active', 'order')
    list_filter = ('menu', 'is_active')
    search_fields = ('name', 'url', 'description')
    ordering = ('menu', 'order', 'name')

@admin.register(GroupModulePermission)
class GroupModulePermissionAdmin(admin.ModelAdmin):
    list_display = ('group', 'module')
    list_filter = ('group', 'module')
    filter_horizontal = ('permissions',)


# from django import forms
# from .models import GroupModulePermission

# class GroupModulePermissionAdminForm(forms.ModelForm):
#     class Meta:
#         model = GroupModulePermission
#         fields = '__all__'

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         # Si ya hay un módulo seleccionado (en edición o POST)
#         if 'module' in self.data:
#             try:
#                 module_id = int(self.data.get('module'))
#                 module = self.fields['module'].queryset.get(pk=module_id)
#                 self.fields['permissions'].queryset = module.permissions.all()
#             except Exception:
#                 self.fields['permissions'].queryset = self.fields['permissions'].queryset.none()
#         elif self.instance.pk:
#             self.fields['permissions'].queryset = self.instance.module.permissions.all()
#         else:
#             self.fields['permissions'].queryset = self.fields['permissions'].queryset.none()

# @admin.register(GroupModulePermission)
# class GroupModulePermissionAdmin(admin.ModelAdmin):
#     form = GroupModulePermissionAdminForm
#     list_display = ('group', 'module')
#     list_filter = ('group', 'module')
#     filter_horizontal = ('permissions',)