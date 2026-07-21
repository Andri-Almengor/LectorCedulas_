# Lector de Cédulas

Aplicación de escritorio para Windows que automatiza la lectura de cédulas costarricenses y el llenado de formularios.

## Funcionalidades

- Lectura automática mediante dispositivos conectados por puerto serial.
- Compatibilidad con cédulas binarias, documentos CSV, códigos QR y estructuras mDoc.
- Validación de datos para evitar escribir lecturas incompletas o no reconocidas.
- Configuraciones personalizadas de campos, orden y tabulaciones.
- Selección de dos configuraciones favoritas y cambio rápido con `Ctrl + Alt + C`.
- Herramientas para capturar y analizar nuevos formatos de documentos.
- Dashboard para administrar clientes, licencias, actualizaciones e instaladores.

## Estructura de configuraciones

- `configs/formularios/`: configuraciones seleccionables para completar formularios.
- `configs/sistema/`: configuración activa, favoritas y último puerto COM.
- `configs/formatos/`: catálogo de formatos de documentos reconocidos.

Las configuraciones de versiones anteriores se migran automáticamente sin eliminar archivos existentes.

## Tecnologías

Python, Tkinter, PySerial, PyAutoGUI, Pillow, Pystray, Requests, BeautifulSoup, JSON, PyInstaller e Inno Setup.

## Ejecución

1. Instalar Python 3.10 o superior.
2. Ejecutar `EJECUTAR_DASHBOARD.bat` para abrir el dashboard con Python.
3. Para generar el ejecutable del dashboard, ejecutar `installer/generar_dashboard_exe.bat`.
4. El resultado se crea en `dist_dashboard/DashboardInstaladores.exe`.

## Notas

- Las actualizaciones conservan la licencia y la carpeta `configs`.
- Las lecturas no reconocidas se guardan en registros de diagnóstico y no se escriben en el formulario.
- El proyecto utiliza una identidad visual genérica y no está asociado públicamente con ninguna empresa.
