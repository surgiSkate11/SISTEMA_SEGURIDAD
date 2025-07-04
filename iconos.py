"""
HealthFlow Pro - Sistema de Iconos
Iconos organizados por categorías con soporte para FontAwesome y Bootstrap Icons
"""

class HealthFlowIcons:
    """
    Clase para gestionar iconos del sistema HealthFlow Pro
    Incluye iconos FontAwesome (fas) y Bootstrap Icons (bi)
    """
    
    # ==================== GESTIÓN DE USUARIOS Y SEGURIDAD ====================
    USUARIOS = {
        'usuario_individual': {
            'fontawesome': 'fas fa-user',
            'bootstrap': 'bi bi-person'
        },
        'lista_usuarios': {
            'fontawesome': 'fas fa-users',
            'bootstrap': 'bi bi-people'
        },
        'agregar_usuario': {
            'fontawesome': 'fas fa-user-plus',
            'bootstrap': 'bi bi-person-plus'
        },
        'editar_usuario': {
            'fontawesome': 'fas fa-user-edit',
            'bootstrap': 'bi bi-person-gear'
        },
        'eliminar_usuario': {
            'fontawesome': 'fas fa-user-times',
            'bootstrap': 'bi bi-person-x'
        },
        'usuario_activo': {
            'fontawesome': 'fas fa-user-check',
            'bootstrap': 'bi bi-person-check'
        }
    }
    
    GRUPOS = {
        'gestion_grupos': {
            'fontawesome': 'fas fa-users-cog',
            'bootstrap': 'bi bi-people-fill'
        },
        'grupos_sistema': {
            'fontawesome': 'fas fa-layer-group',
            'bootstrap': 'bi bi-layers'
        },
        'agrupar': {
            'fontawesome': 'fas fa-object-group',
            'bootstrap': 'bi bi-collection'
        },
        'jerarquia_grupos': {
            'fontawesome': 'fas fa-sitemap',
            'bootstrap': 'bi bi-diagram-3'
        }
    }
    
    PERMISOS = {
        'permisos': {
            'fontawesome': 'fas fa-shield-alt',
            'bootstrap': 'bi bi-shield'
        },
        'seguridad_usuario': {
            'fontawesome': 'fas fa-user-shield',
            'bootstrap': 'bi bi-person-lock'
        },
        'claves_acceso': {
            'fontawesome': 'fas fa-key',
            'bootstrap': 'bi bi-key'
        },
        'bloquear': {
            'fontawesome': 'fas fa-lock',
            'bootstrap': 'bi bi-lock'
        },
        'desbloquear': {
            'fontawesome': 'fas fa-unlock',
            'bootstrap': 'bi bi-unlock'
        },
        'usuario_bloqueado': {
            'fontawesome': 'fas fa-user-lock',
            'bootstrap': 'bi bi-person-x'
        }
    }
    
    ROLES = {
        'roles': {
            'fontawesome': 'fas fa-user-tag',
            'bootstrap': 'bi bi-person-badge'
        },
        'etiquetas_roles': {
            'fontawesome': 'fas fa-tags',
            'bootstrap': 'bi bi-tags'
        },
        'administrador': {
            'fontawesome': 'fas fa-crown',
            'bootstrap': 'bi bi-person-workspace'
        },
        'supervisor': {
            'fontawesome': 'fas fa-user-tie',
            'bootstrap': 'bi bi-person-check'
        }
    }
    
    # ==================== MÓDULOS MÉDICOS PRINCIPALES ====================
    SEGURIDAD = {
        'seguridad_sistema': {
            'fontawesome': 'fas fa-shield-virus',
            'bootstrap': 'bi bi-shield-check'
        },
        'autenticacion': {
            'fontawesome': 'fas fa-fingerprint',
            'bootstrap': 'bi bi-fingerprint'
        },
        'acceso_restringido': {
            'fontawesome': 'fas fa-user-secret',
            'bootstrap': 'bi bi-incognito'
        }
    }
    
    MEDICOS = {
        'medicos': {
            'fontawesome': 'fas fa-user-md',
            'bootstrap': 'bi bi-person-heart'
        },
        'consultas': {
            'fontawesome': 'fas fa-stethoscope',
            'bootstrap': 'bi bi-heart-pulse'
        },
        'cardiologia': {
            'fontawesome': 'fas fa-heartbeat',
            'bootstrap': 'bi bi-heart'
        },
        'neurologia': {
            'fontawesome': 'fas fa-brain',
            'bootstrap': 'bi bi-brain'
        },
        'oftalmologia': {
            'fontawesome': 'fas fa-eye',
            'bootstrap': 'bi bi-eye'
        },
        'odontologia': {
            'fontawesome': 'fas fa-tooth',
            'bootstrap': 'bi bi-tooth'
        }
    }
    
    ASISTENTES = {
        'enfermeras': {
            'fontawesome': 'fas fa-user-nurse',
            'bootstrap': 'bi bi-person-plus-fill'
        },
        'asistentes': {
            'fontawesome': 'fas fa-hands-helping',
            'bootstrap': 'bi bi-people'
        },
        'tareas_asistente': {
            'fontawesome': 'fas fa-clipboard-list',
            'bootstrap': 'bi bi-clipboard-check'
        },
        'cuidados': {
            'fontawesome': 'fas fa-hand-holding-heart',
            'bootstrap': 'bi bi-heart-half'
        }
    }
    
    PACIENTES = {
        'pacientes': {
            'fontawesome': 'fas fa-user-injured',
            'bootstrap': 'bi bi-person-wheelchair'
        },
        'pacientes_especiales': {
            'fontawesome': 'fas fa-wheelchair',
            'bootstrap': 'bi bi-universal-access'
        },
        'pediatria': {
            'fontawesome': 'fas fa-baby',
            'bootstrap': 'bi bi-person'
        },
        'ginecologia': {
            'fontawesome': 'fas fa-female',
            'bootstrap': 'bi bi-gender-female'
        },
        'historial_medico': {
            'fontawesome': 'fas fa-file-medical',
            'bootstrap': 'bi bi-file-medical'
        },
        'identificacion': {
            'fontawesome': 'fas fa-id-card',
            'bootstrap': 'bi bi-card-text'
        }
    }
    
    # ==================== LABORATORIO Y DIAGNÓSTICOS ====================
    LABORATORIO = {
        'laboratorio': {
            'fontawesome': 'fas fa-microscope',
            'bootstrap': 'bi bi-eyedropper'
        },
        'muestras': {
            'fontawesome': 'fas fa-vial',
            'bootstrap': 'bi bi-droplet'
        },
        'analisis': {
            'fontawesome': 'fas fa-flask',
            'bootstrap': 'bi bi-beaker'
        },
        'genetica': {
            'fontawesome': 'fas fa-dna',
            'bootstrap': 'bi bi-diagram-2'
        },
        'rayos_x': {
            'fontawesome': 'fas fa-x-ray',
            'bootstrap': 'bi bi-camera'
        },
        'neumologia': {
            'fontawesome': 'fas fa-lungs',
            'bootstrap': 'bi bi-heart-pulse'
        }
    }
    
    # ==================== FARMACIA Y MEDICAMENTOS ====================
    FARMACIA = {
        'medicamentos': {
            'fontawesome': 'fas fa-pills',
            'bootstrap': 'bi bi-capsule'
        },
        'recetas': {
            'fontawesome': 'fas fa-prescription-bottle',
            'bootstrap': 'bi bi-prescription'
        },
        'inventario': {
            'fontawesome': 'fas fa-capsules',
            'bootstrap': 'bi bi-box'
        },
        'vacunas': {
            'fontawesome': 'fas fa-syringe',
            'bootstrap': 'bi bi-thermometer'
        },
        'farmacia_principal': {
            'fontawesome': 'fas fa-mortar-pestle',
            'bootstrap': 'bi bi-shop'
        }
    }
    
    # ==================== EMERGENCIAS Y URGENCIAS ====================
    EMERGENCIAS = {
        'ambulancia': {
            'fontawesome': 'fas fa-ambulance',
            'bootstrap': 'bi bi-truck'
        },
        'primeros_auxilios': {
            'fontawesome': 'fas fa-first-aid',
            'bootstrap': 'bi bi-bandaid'
        },
        'emergencias': {
            'fontawesome': 'fas fa-heartbeat',
            'bootstrap': 'bi bi-heart-pulse'
        },
        'alertas': {
            'fontawesome': 'fas fa-exclamation-triangle',
            'bootstrap': 'bi bi-exclamation-triangle'
        },
        'llamadas_emergencia': {
            'fontawesome': 'fas fa-phone-alt',
            'bootstrap': 'bi bi-telephone'
        }
    }
    
    # ==================== CITAS Y AGENDA ====================
    CITAS = {
        'citas': {
            'fontawesome': 'fas fa-calendar-check',
            'bootstrap': 'bi bi-calendar-check'
        },
        'nueva_cita': {
            'fontawesome': 'fas fa-calendar-plus',
            'bootstrap': 'bi bi-calendar-plus'
        },
        'horarios': {
            'fontawesome': 'fas fa-clock',
            'bootstrap': 'bi bi-clock'
        },
        'agenda': {
            'fontawesome': 'fas fa-business-time',
            'bootstrap': 'bi bi-calendar2-week'
        }
    }
    
    # ==================== HOSPITALIZACIÓN ====================
    HOSPITALIZACION = {
        'habitaciones': {
            'fontawesome': 'fas fa-bed',
            'bootstrap': 'bi bi-house'
        },
        'cirugias': {
            'fontawesome': 'fas fa-procedures',
            'bootstrap': 'bi bi-scissors'
        },
        'hospital': {
            'fontawesome': 'fas fa-hospital',
            'bootstrap': 'bi bi-building'
        },
        'infraestructura': {
            'fontawesome': 'fas fa-building',
            'bootstrap': 'bi bi-buildings'
        }
    }
    
    # ==================== FACTURACIÓN Y FINANZAS ====================
    FACTURACION = {
        'facturacion': {
            'fontawesome': 'fas fa-file-invoice-dollar',
            'bootstrap': 'bi bi-receipt'
        },
        'pagos': {
            'fontawesome': 'fas fa-credit-card',
            'bootstrap': 'bi bi-credit-card'
        },
        'recibos': {
            'fontawesome': 'fas fa-receipt',
            'bootstrap': 'bi bi-receipt-cutoff'
        },
        'ingresos': {
            'fontawesome': 'fas fa-money-bill-wave',
            'bootstrap': 'bi bi-cash'
        },
        'calculos': {
            'fontawesome': 'fas fa-calculator',
            'bootstrap': 'bi bi-calculator'
        }
    }
    
    # ==================== INVENTARIO ====================
    INVENTARIO = {
        'inventario': {
            'fontawesome': 'fas fa-boxes',
            'bootstrap': 'bi bi-boxes'
        },
        'almacen': {
            'fontawesome': 'fas fa-warehouse',
            'bootstrap': 'bi bi-building'
        },
        'suministros': {
            'fontawesome': 'fas fa-truck',
            'bootstrap': 'bi bi-truck'
        },
        'codigos': {
            'fontawesome': 'fas fa-barcode',
            'bootstrap': 'bi bi-upc'
        }
    }
    
    # ==================== REPORTES Y ANÁLISIS ====================
    REPORTES = {
        'graficos': {
            'fontawesome': 'fas fa-chart-line',
            'bootstrap': 'bi bi-graph-up'
        },
        'estadisticas': {
            'fontawesome': 'fas fa-chart-bar',
            'bootstrap': 'bi bi-bar-chart'
        },
        'distribucion': {
            'fontawesome': 'fas fa-chart-pie',
            'bootstrap': 'bi bi-pie-chart'
        },
        'analytics': {
            'fontawesome': 'fas fa-analytics',
            'bootstrap': 'bi bi-graph-up-arrow'
        },
        'reportes': {
            'fontawesome': 'fas fa-file-chart',
            'bootstrap': 'bi bi-file-bar-graph'
        },
        'imprimir': {
            'fontawesome': 'fas fa-print',
            'bootstrap': 'bi bi-printer'
        },
        'exportar': {
            'fontawesome': 'fas fa-file-export',
            'bootstrap': 'bi bi-download'
        },
        'descargar': {
            'fontawesome': 'fas fa-download',
            'bootstrap': 'bi bi-cloud-download'
        }
    }
    
    # ==================== CONFIGURACIÓN Y SISTEMA ====================
    CONFIGURACION = {
        'configuracion': {
            'fontawesome': 'fas fa-cogs',
            'bootstrap': 'bi bi-gear'
        },
        'herramientas': {
            'fontawesome': 'fas fa-tools',
            'bootstrap': 'bi bi-tools'
        },
        'ajustes': {
            'fontawesome': 'fas fa-sliders-h',
            'bootstrap': 'bi bi-sliders'
        },
        'mantenimiento': {
            'fontawesome': 'fas fa-wrench',
            'bootstrap': 'bi bi-wrench'
        }
    }
    
    SISTEMA = {
        'servidor': {
            'fontawesome': 'fas fa-server',
            'bootstrap': 'bi bi-server'
        },
        'base_datos': {
            'fontawesome': 'fas fa-database',
            'bootstrap': 'bi bi-database'
        },
        'nube': {
            'fontawesome': 'fas fa-cloud',
            'bootstrap': 'bi bi-cloud'
        },
        'respaldo': {
            'fontawesome': 'fas fa-backup',
            'bootstrap': 'bi bi-shield-check'
        }
    }
    
    MENUS = {
        'menu_principal': {
            'fontawesome': 'fas fa-bars',
            'bootstrap': 'bi bi-list'
        },
        'lista_menus': {
            'fontawesome': 'fas fa-list',
            'bootstrap': 'bi bi-menu-button-wide'
        },
        'agregar_menu': {
            'fontawesome': 'fas fa-plus-square',
            'bootstrap': 'bi bi-plus-square'
        },
        'editar_menu': {
            'fontawesome': 'fas fa-edit',
            'bootstrap': 'bi bi-pencil'
        }
    }
    
    # ==================== COMUNICACIÓN Y NOTIFICACIONES ====================
    COMUNICACION = {
        'notificaciones': {
            'fontawesome': 'fas fa-bell',
            'bootstrap': 'bi bi-bell'
        },
        'mensajes': {
            'fontawesome': 'fas fa-envelope',
            'bootstrap': 'bi bi-envelope'
        },
        'telefono': {
            'fontawesome': 'fas fa-phone',
            'bootstrap': 'bi bi-telephone'
        },
        'videollamada': {
            'fontawesome': 'fas fa-video',
            'bootstrap': 'bi bi-camera-video'
        },
        'chat': {
            'fontawesome': 'fas fa-comments',
            'bootstrap': 'bi bi-chat'
        },
        'anuncios': {
            'fontawesome': 'fas fa-bullhorn',
            'bootstrap': 'bi bi-megaphone'
        }
    }
    
    # ==================== ESPECIALIDADES MÉDICAS ====================
    ESPECIALIDADES = {
        'radiologia': {
            'fontawesome': 'fas fa-x-ray',
            'bootstrap': 'bi bi-camera'
        },
        'neumologia': {
            'fontawesome': 'fas fa-lungs',
            'bootstrap': 'bi bi-heart-pulse'
        },
        'traumatologia': {
            'fontawesome': 'fas fa-bone',
            'bootstrap': 'bi bi-bandaid'
        },
        'nefrologia': {
            'fontawesome': 'fas fa-kidney',
            'bootstrap': 'bi bi-droplet'
        },
        'oncologia': {
            'fontawesome': 'fas fa-ribbon',
            'bootstrap': 'bi bi-heart'
        },
        'pediatria': {
            'fontawesome': 'fas fa-child',
            'bootstrap': 'bi bi-person'
        },
        'ginecologia': {
            'fontawesome': 'fas fa-venus',
            'bootstrap': 'bi bi-gender-female'
        },
        'urologia': {
            'fontawesome': 'fas fa-mars',
            'bootstrap': 'bi bi-gender-male'
        }
    }
    
    # ==================== MÉTODOS UTILITARIOS ====================
    
    @classmethod
    def get_icon(cls, categoria, nombre, tipo='fontawesome'):
        """
        Obtiene un icono específico por categoría y nombre
        
        Args:
            categoria (str): Nombre de la categoría (ej: 'USUARIOS', 'MEDICOS')
            nombre (str): Nombre del icono específico
            tipo (str): Tipo de icono ('fontawesome' o 'bootstrap')
        
        Returns:
            str: Clase CSS del icono
        """
        try:
            categoria_obj = getattr(cls, categoria.upper())
            icono = categoria_obj.get(nombre, {})
            return icono.get(tipo, '')
        except AttributeError:
            return ''
    
    @classmethod
    def get_html_icon(cls, categoria, nombre, tipo='fontawesome', clase_adicional='healthflow-icon'):
        """
        Genera el HTML completo para un icono
        
        Args:
            categoria (str): Nombre de la categoría
            nombre (str): Nombre del icono específico
            tipo (str): Tipo de icono ('fontawesome' o 'bootstrap')
            clase_adicional (str): Clases CSS adicionales
        
        Returns:
            str: HTML completo del icono
        """
        icono_clase = cls.get_icon(categoria, nombre, tipo)
        if icono_clase:
            return f'<i class="{icono_clase} {clase_adicional}"></i>'
        return ''
    
    @classmethod
    def listar_iconos_categoria(cls, categoria, tipo='fontawesome'):
        """
        Lista todos los iconos de una categoría específica
        
        Args:
            categoria (str): Nombre de la categoría
            tipo (str): Tipo de icono a listar
        
        Returns:
            dict: Diccionario con nombres e iconos de la categoría
        """
        try:
            categoria_obj = getattr(cls, categoria.upper())
            return {nombre: iconos.get(tipo, '') for nombre, iconos in categoria_obj.items()}
        except AttributeError:
            return {}
    
    @classmethod
    def get_all_categories(cls):
        """
        Obtiene todas las categorías disponibles
        
        Returns:
            list: Lista de nombres de categorías
        """
        return [attr for attr in dir(cls) if not attr.startswith('_') and attr.isupper()]

# ==================== EJEMPLOS DE USO ====================

def ejemplos_uso():
    """
    Ejemplos de cómo usar la clase HealthFlowIcons
    """
    
    # Obtener un icono específico
    icono_usuario = HealthFlowIcons.get_icon('USUARIOS', 'usuario_individual', 'fontawesome')
    print(f"Icono de usuario: {icono_usuario}")
    
    # Generar HTML completo
    html_medico = HealthFlowIcons.get_html_icon('MEDICOS', 'medicos', 'bootstrap')
    print(f"HTML médico: {html_medico}")
    
    # Listar todos los iconos de una categoría
    iconos_farmacia = HealthFlowIcons.listar_iconos_categoria('FARMACIA', 'fontawesome')
    print(f"Iconos de farmacia: {iconos_farmacia}")
    
    # Obtener todas las categorías
    categorias = HealthFlowIcons.get_all_categories()
    print(f"Categorías disponibles: {categorias}")

if __name__ == "__main__":
    ejemplos_uso()