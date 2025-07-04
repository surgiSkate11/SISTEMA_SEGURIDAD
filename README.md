# Sistema Médico - Security

Un sistema médico integral desarrollado con Django que incluye gestión de pacientes, doctores, citas médicas y seguridad avanzada.

## Características

- 🏥 **Gestión de Pacientes**: Registro y seguimiento completo de pacientes
- 👨‍⚕️ **Gestión de Doctores**: Administración de personal médico y especialidades
- 📅 **Sistema de Citas**: Programación y gestión de citas médicas
- 💊 **Gestión de Medicamentos**: Control de inventario farmacéutico
- 🔐 **Seguridad Avanzada**: Sistema de autenticación y autorización robusto
- 📊 **Reportes y Estadísticas**: Dashboard con métricas importantes

## Tecnologías Utilizadas

- **Backend**: Django (Python)
- **Base de Datos**: SQLite (desarrollo)
- **Frontend**: HTML, CSS, JavaScript
- **Seguridad**: Django Security Framework
- **UI Framework**: Bootstrap (opcional)

## Instalación

1. **Clonar el repositorio**
   ```bash
   git clone https://github.com/surgiSkate11/System_Medical-Security.git
   cd System_Medical-Security
   ```

2. **Crear entorno virtual**
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   # source venv/bin/activate  # Linux/Mac
   ```

3. **Instalar dependencias**
   ```bash
   pip install -r dependencias.txt
   ```

4. **Configurar base de datos**
   ```bash
   cd app_security
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Crear superusuario**
   ```bash
   python manage.py createsuperuser
   ```

6. **Ejecutar servidor**
   ```bash
   python manage.py runserver
   ```

## Estructura del Proyecto

```
SYSTEM_MEDICAL/
├── app_security/           # Aplicación principal Django
│   ├── applications/       # Aplicaciones del sistema
│   │   ├── core/          # Funcionalidades principales
│   │   ├── doctor/        # Gestión de doctores
│   │   └── security/      # Sistema de seguridad
│   ├── static/            # Archivos estáticos
│   ├── templates/         # Plantillas HTML
│   └── manage.py          # Script de gestión Django
├── venv/                  # Entorno virtual (no incluido en repo)
├── dependencias.txt       # Dependencias del proyecto
└── README.md             # Este archivo
```

## Uso

1. Acceder al sistema en `http://localhost:8000`
2. Iniciar sesión con las credenciales de superusuario
3. Navegar por los diferentes módulos del sistema
4. Gestionar pacientes, doctores, citas y medicamentos

## Contribución

1. Fork el proyecto
2. Crear una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -am 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Crear un Pull Request

## Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## Contacto

- **Desarrollador**: surgiSkate11
- **GitHub**: [https://github.com/surgiSkate11](https://github.com/surgiSkate11)
- **Proyecto**: [https://github.com/surgiSkate11/System_Medical-Security](https://github.com/surgiSkate11/System_Medical-Security)

---

⚕️ **Sistema Médico desarrollado con Django** ⚕️
