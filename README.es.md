[Español](README.es.md) | [English](README.en.md)

---

# FlowShotCLI

FlowShotCLI es un grabador estricto y elegante de flujos de terminal. Captura los comandos de tu shell y los convierte en scripts limpios, reutilizables y seguros.

A diferencia de herramientas que graban la salida de una sesion, FlowShotCLI se centra en la logica: los comandos ejecutados.

## Caracteristicas

- Grabacion no intrusiva desde historial `.zsh_history` o `.bash_history`.
- Limpieza de duplicados consecutivos.
- Exportacion con `set -euo pipefail`.
- Pasos y secciones con `flowshot step`.
- Deteccion de variables repetidas.
- Validadores para comandos destructivos o interactivos.
- Sanitizado de secretos y rutas personales.
- Reproductor interactivo paso a paso.
- IA opcional con Ollama local.

## Instalacion

Requiere Python 3.8 o superior.

```bash
pip install flowshot-cli
```

## Inicio rapido

```bash
flowshot start
# ejecuta tus comandos
flowshot step "Build Phase"
flowshot stop
flowshot list
flowshot export --bash --output setup.sh --preset safe
```

## Presets de exportacion

- `local`: modo estricto estandar.
- `safe`: confirmacion interactiva para cada comando.
- `ci`: salida detallada con `set -x`.

## Casos de uso

- Convertir una sesion manual en un script reproducible.
- Documentar pasos de instalacion.
- Preparar automatizaciones seguras para equipo o CI.
