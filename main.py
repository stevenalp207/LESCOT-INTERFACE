import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import pygame
import serial
import threading
import json
import time
import os

# Inicializa pygame para reproducir audio
pygame.mixer.init()

def reproducir_audio():
    """Reproduce el archivo de audio."""
    try:
        pygame.mixer.music.load("INSTRUCCIONES.mp3")
        pygame.mixer.music.set_volume(1.0)
        pygame.mixer.music.play()
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo reproducir el audio: {e}")

# Configuración de la ventana principal
ventana = tk.Tk()
ventana.title("Interfaz Raspberry Pi")
ventana.geometry("1920x1080")
ventana.attributes("-fullscreen", True)

def cerrar_con_esc(event):
    if puerto_serie and puerto_serie.is_open:
        puerto_serie.close()  # Cierra el puerto al salir
    ventana.destroy()

ventana.bind("<Escape>", cerrar_con_esc)

# Cargar imagen de fondo
try:
    imagen_fondo = Image.open("INTERFAZ-02.png").resize((1920, 1080), Image.Resampling.LANCZOS)
    fondo = ImageTk.PhotoImage(imagen_fondo)
    tk.Label(ventana, image=fondo).place(x=0, y=0, relwidth=1, relheight=1)
except Exception as e:
    messagebox.showwarning("Advertencia", f"No se pudo cargar la imagen de fondo: {e}")

# Cargar imagen del botón
try:
    imagen_boton = Image.open("INTERFAZ-05.png").resize((450, 85), Image.Resampling.LANCZOS)
    boton_img = ImageTk.PhotoImage(imagen_boton)
    tk.Button(
        ventana, image=boton_img, command=reproducir_audio,
        bg="#214561", borderwidth=0, activebackground="#214561"
    ).place(x=166, y=490, width=450, height=85)
except Exception as e:
    messagebox.showwarning("Advertencia", f"No se pudo cargar la imagen del botón: {e}")

# Cargar imágenes de estado
try:
    imagen_bien = Image.open("INTERFAZ-03.png").resize((865, 57), Image.Resampling.LANCZOS)
    imagen_mal = Image.open("INTERFAZ-04.png").resize((865, 57), Image.Resampling.LANCZOS)
    imagen_estado_bien = ImageTk.PhotoImage(imagen_bien)
    imagen_estado_mal = ImageTk.PhotoImage(imagen_mal)
except Exception as e:
    messagebox.showwarning("Advertencia", f"No se pudieron cargar las imágenes de estado: {e}")

# Diccionario para almacenar las imágenes de las señas
imagenes_senas = {}

def cargar_imagenes_senas():
    """Carga las imágenes de las señas desde la carpeta PNG."""
    try:
        for letra in "ABCDEFGHIKLMNOPQRSTUVWXYZ":
            ruta_imagen = os.path.join("png", f"ABC_{letra} copia.png")
            imagen = Image.open(ruta_imagen).resize((449, 641), Image.Resampling.LANCZOS)
            imagenes_senas[letra] = ImageTk.PhotoImage(imagen)
    except Exception as e:
        messagebox.showwarning("Advertencia", f"No se pudieron cargar todas las imágenes: {e}")

# Llamada para cargar las imágenes al inicio
cargar_imagenes_senas()

# Configuración del puerto serie
puerto_serie = None
try:
    puerto_serie = serial.Serial('COM5', baudrate=115200, timeout=1)  # Ajusta el puerto si es necesario
except serial.SerialException as e:
    messagebox.showerror("Error", f"No se pudo abrir el puerto serie: {e}")
    ventana.destroy()

label_datos = tk.Label(ventana, text="SEÑA DETECTADA: NINGUNA", font=("Montserrat", 24, "bold"), bg="#214561",
                       fg="white")
label_datos.place(x=166, y=600)

# Label para mostrar el estado
label_estado = tk.Label(ventana)
label_estado.place(x=960, y=50)  # Colocar arriba de la imagen de fondo

# Label para mostrar la seña detectada
label_sena = tk.Label(ventana)
label_sena.place(x=1070, y=220)  # Colocar arriba de la imagen de fondo

def actualizar_label(valor, estado):
    """Actualiza el label de texto y la imagen de la seña detectada."""
    global imagen_estado_bien, imagen_estado_mal

    label_datos.config(text=f"SEÑA DETECTADA: {valor}")

    # Actualiza la imagen del estado
    if estado == "BIEN":
        label_estado.config(image=imagen_estado_bien)
        label_estado.image = imagen_estado_bien  # Evita recolección de basura
    elif estado == "MAL":
        label_estado.config(image=imagen_estado_mal)
        label_estado.image = imagen_estado_mal  # Evita recolección de basura

    # Cambia la imagen de la seña detectada si existe en el diccionario
    if valor in imagenes_senas:
        label_sena.config(image=imagenes_senas[valor])
        label_sena.image = imagenes_senas[valor]  # Evita recolección de basura
    else:
        label_sena.config(image='')  # Limpia si no se reconoce la seña

def leer_datos_serie():
    """Lee datos del puerto serie en un hilo separado."""
    while True:
        try:
            if puerto_serie.in_waiting > 0:
                json_data = puerto_serie.readline().decode('utf-8', errors='ignore').strip()
                print(f"DATO JSON: {json_data}")  # Depuración

                # Intenta cargar los datos como JSON
                try:
                    sena = json.loads(json_data)  # Cargar el JSON
                    print(f"Seña detectada: {sena['sena']}, Estado: {sena['estado']}")
                    ventana.after(0, actualizar_label, sena['sena'], sena['estado'])
                except json.JSONDecodeError:
                    print(f"Error al decodificar JSON: {json_data}")

            time.sleep(0.1)  # Pequeña pausa para evitar saturación
        except serial.SerialException as e:
            print(f"Error en el puerto serie: {e}")
            break  # Sale del bucle si hay un error de puerto serie

# Iniciar el hilo de lectura
hilo_lectura = threading.Thread(target=leer_datos_serie, daemon=True)
hilo_lectura.start()

# Ejecutar la interfaz gráfica
ventana.mainloop()
