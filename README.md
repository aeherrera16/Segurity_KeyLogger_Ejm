# Segurity_KeyLogger_Ejm

Este repositorio contiene un ejemplo educativo de un keylogger en Python. El propósito declarado es únicamente educativo: aprender sobre captura de eventos de teclado, persistencia en Windows y manejo de logs. No uses este software en equipos que no sean de tu propiedad o sin permiso explícito — el uso no autorizado puede ser ilegal.

## Contenido del repositorio

- `keylogger.py` — Código fuente del keylogger en Python.
- `requirements.txt` — Dependencias necesarias (p. ej. `pynput`).
- `.gitignore` — Archivos y carpetas excluidas; `keylog.txt` está en la lista y NO debe subirse.

## Advertencia legal y ética

Este proyecto es para fines educativos únicamente. Antes de ejecutar cualquier componente:

- Asegúrate de tener permiso explícito del propietario del equipo.
- Ejecuta pruebas únicamente en un entorno controlado (máquina virtual o equipo de laboratorio).
- No lo uses para recolectar datos de terceros sin consentimiento.

El autor del repositorio no se hace responsable por el uso indebido del software.

## Requisitos

- Python 3.8+ (se recomienda 3.10 o superior).
- Instalar dependencias:

```powershell
pip install -r requirements.txt
```

## Cómo ejecutar (modo seguro / educativo)

1. Revisa el código `keylogger.py`, especialmente la función `add_to_startup()` que modifica el registro de Windows para persistencia. Si solo quieres probar localmente, comenta o elimina la llamada a `add_to_startup()` en la sección `if __name__ == '__main__':`.

2. Ejecuta el script en una máquina de pruebas:

```powershell
python keylogger.py
```

3. El programa escribe las teclas (formateadas por palabras) en `keylog.txt` en la misma carpeta. Presiona `ESC` para detener la captura.

Nota: `keylog.txt` está incluido en `.gitignore` para evitar subir datos sensibles accidentalmente.

## Modo de prueba sugerido

Para evitar cambios en el sistema (registro), puedes temporalmente modificar el bloque principal así:

```python
# if __name__ == '__main__':
#     #add_to_startup()
#     log_startup()
#     with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
#         listener.join()
```

O simplemente comentar la llamada a `add_to_startup()`.
