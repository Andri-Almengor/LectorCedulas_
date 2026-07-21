from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
WORKFLOW = ROOT / ".github" / "workflows" / "remove_branding_once.yml"
TEXT_EXTENSIONS = {
    ".py", ".txt", ".md", ".bat", ".cmd", ".json", ".iss",
    ".yml", ".yaml", ".toml", ".ini", ".cfg", ".spec",
}

README = """# Lector de Cédulas

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
"""

EXACT_REPLACEMENTS = [
    ("Digital Management Systems, S.A.", "Proyecto independiente"),
    ("Digital Management Systems", "Proyecto independiente"),
    ("DMS - Lector QR | Dashboard de Instaladores", "Lector de Cédulas | Dashboard de Instaladores"),
    ("DMS - Lector QR", "Lector de Cédulas"),
    ("DMS - Configuraciones", "Configuraciones del lector"),
    ("DMS - Cambio rápido", "Cambio rápido de configuración"),
    ("DMS - Capturar nuevo formato de documento", "Capturar nuevo formato de documento"),
    ("DMS - Capturador de otras cédulas", "Capturador de otras cédulas"),
    ("DMS Lector de Cédulas", "Lector de Cédulas"),
    ("Lector Cédulas DMS", "Lector de Cédulas"),
    ("LectorCedulasDMS", "LectorCedulas"),
    ("DashboardInstaladoresDMS", "DashboardInstaladores"),
    ("DMS_icono_circulo_i.ico", "icono.ico"),
    ("DMS_QRReader", "LectorCedulas_QRReader"),
    ("DMS_QR", "LectorCedulas_QR"),
]

CLEANUP_REPLACEMENTS = [
    ("LectorCedulas - Lector QR | Dashboard de Instaladores", "Lector de Cédulas | Dashboard de Instaladores"),
    ("LectorCedulas - Lector QR", "Lector de Cédulas"),
    ("LectorCedulas - Configuraciones", "Configuraciones del lector"),
    ("LectorCedulas - Cambio rápido", "Cambio rápido de configuración"),
    ("LectorCedulas - Capturar nuevo formato de documento", "Capturar nuevo formato de documento"),
    ("LectorCedulas - Capturador de otras cédulas", "Capturador de otras cédulas"),
    ("Lector Cédulas LectorCedulas", "Lector de Cédulas"),
    ("LectorCedulas Lector de Cédulas", "Lector de Cédulas"),
    ("DashboardInstaladoresLectorCedulas", "DashboardInstaladores"),
    ("LectorCedulasLectorCedulas", "LectorCedulas"),
]


def decode_text(data: bytes) -> tuple[str, str] | None:
    if b"\x00" in data:
        return None
    for encoding in ("utf-8-sig", "utf-8", "cp1252", "latin-1"):
        try:
            return data.decode(encoding), encoding
        except UnicodeDecodeError:
            continue
    return None


def clean_text(text: str) -> str:
    cleaned = text
    for old, new in EXACT_REPLACEMENTS:
        cleaned = re.sub(re.escape(old), new, cleaned, flags=re.IGNORECASE)

    # Elimina cualquier referencia textual restante de la sigla de la marca,
    # incluso cuando forma parte de identificadores técnicos.
    cleaned = re.sub(r"(?i)dms", "LectorCedulas", cleaned)

    for old, new in CLEANUP_REPLACEMENTS:
        cleaned = cleaned.replace(old, new)

    return cleaned


def clean_repository_text() -> None:
    excluded = {Path(__file__).resolve(), WORKFLOW.resolve()}
    for path in sorted(ROOT.rglob("*")):
        if not path.is_file() or ".git" in path.parts:
            continue
        if path.resolve() in excluded:
            continue
        if path.name in {"README.md", "README.txt"}:
            continue
        if path.suffix.lower() not in TEXT_EXTENSIONS and path.name not in {"requirements.txt"}:
            continue

        decoded = decode_text(path.read_bytes())
        if decoded is None:
            continue
        text, _ = decoded
        cleaned = clean_text(text)
        if cleaned != text:
            path.write_text(cleaned, encoding="utf-8", newline="\n")


def create_generic_icon() -> None:
    from PIL import Image, ImageDraw

    assets = ROOT / "template" / "assets"
    assets.mkdir(parents=True, exist_ok=True)

    for icon in assets.glob("*.ico"):
        icon.unlink()

    size = 256
    image = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle((16, 28, 240, 228), radius=30, fill=(46, 95, 170, 255))
    draw.ellipse((42, 68, 106, 132), fill=(255, 255, 255, 255))
    draw.rounded_rectangle((34, 132, 114, 190), radius=22, fill=(255, 255, 255, 255))
    draw.rounded_rectangle((132, 74, 216, 91), radius=8, fill=(255, 255, 255, 255))
    draw.rounded_rectangle((132, 112, 216, 129), radius=8, fill=(255, 255, 255, 255))
    draw.rounded_rectangle((132, 150, 198, 167), radius=8, fill=(255, 255, 255, 255))
    image.save(assets / "icono.ico", format="ICO", sizes=[(16, 16), (24, 24), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)])


def rename_branded_paths() -> None:
    paths = sorted(
        (p for p in ROOT.rglob("*") if ".git" not in p.parts and "dms" in p.name.lower()),
        key=lambda p: len(p.parts),
        reverse=True,
    )
    for path in paths:
        new_name = re.sub(r"(?i)dms", "LectorCedulas", path.name)
        destination = path.with_name(new_name)
        if destination.exists():
            if path.is_file():
                path.unlink()
            continue
        path.rename(destination)


def verify_clean() -> None:
    failures: list[str] = []
    excluded = {Path(__file__).resolve(), WORKFLOW.resolve()}
    for path in ROOT.rglob("*"):
        if ".git" in path.parts or not path.is_file() or path.resolve() in excluded:
            continue
        if "dms" in path.name.lower():
            failures.append(f"Nombre de archivo: {path.relative_to(ROOT)}")
            continue
        decoded = decode_text(path.read_bytes())
        if decoded is None:
            continue
        text, _ = decoded
        if re.search(r"(?i)dms", text):
            failures.append(f"Contenido: {path.relative_to(ROOT)}")
    if failures:
        raise RuntimeError("Quedaron referencias de marca:\n" + "\n".join(failures))


def remove_one_time_files() -> None:
    if WORKFLOW.exists():
        WORKFLOW.unlink()
    script = Path(__file__).resolve()
    if script.exists():
        script.unlink()


if __name__ == "__main__":
    clean_repository_text()
    (ROOT / "README.md").write_text(README, encoding="utf-8", newline="\n")
    (ROOT / "README.txt").write_text(README, encoding="utf-8", newline="\n")
    create_generic_icon()
    rename_branded_paths()
    verify_clean()
    remove_one_time_files()
