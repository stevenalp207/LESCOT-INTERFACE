# Interfaz Raspberry Pi

Este proyecto es una interfaz gráfica en Python utilizando Tkinter para interactuar con una Raspberry Pi mediante comunicación serial.

## Características
- Carga y muestra imágenes de fondo y botones.
- Reproduce un archivo de audio con instrucciones.
- Conexión con un puerto serie para recibir datos en formato JSON.
- Visualización de imágenes correspondientes a las señas detectadas.
- Estado de la seña mostrada en pantalla.

## Requisitos
- Python 3.x
- Tkinter (incluido en Python por defecto)
- Pygame
- Pillow
- PySerial

Puedes instalar las dependencias ejecutando:
```bash
pip install pygame pillow pyserial
```

## Uso
1. Asegúrate de que la Raspberry Pi esté enviando datos al puerto serie especificado (por defecto `COM5`).
2. Ejecuta el script:
```bash
python script.py
```
3. La interfaz mostrará la imagen de fondo y permitirá reproducir el audio de instrucciones.
4. Si se detecta una seña, se mostrará en pantalla junto con su estado.
5. Presiona `Escape` para salir de la aplicación.

## Estructura de Datos Recibidos
El script espera recibir datos en formato JSON con la siguiente estructura:
```json
{
  "sena": "A",
  "estado": "BIEN"
}
```
- `sena`: Letra detectada.
- `estado`: Puede ser `BIEN` o `MAL`, indicando la precisión de la detección.

## Notas
- Asegúrate de que los archivos `INSTRUCCIONES.mp3`, `INTERFAZ-02.png`, `INTERFAZ-03.png`, `INTERFAZ-04.png`, y `INTERFAZ-05.png` estén en la misma carpeta que el script.
- Las imágenes de las señas deben estar en la carpeta `png/` y seguir la nomenclatura `ABC_<letra> copia.png`.
- Si el puerto serie no está disponible, la aplicación mostrará un mensaje de error y se cerrará.

## Licencia
Este proyecto se distribuye bajo la licencia MIT.

