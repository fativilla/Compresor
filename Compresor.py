from PIL import Image
import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import webbrowser

def compress_image(input_path, output_path, quality=60):
    """
    Comprime una imagen y la guarda en el directorio especificado.
    
    :param input_path: Ruta de la imagen original.
    :param output_path: Ruta donde se guardará la imagen comprimida.
    :param quality: Calidad de la imagen comprimida (1-100).
    """
    with Image.open(input_path) as img:
        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")
        img.save(output_path, "JPEG", quality=quality)

def compress_images_in_folder(folder_path, output_folder, quality=60, progress_var=None, progress_bar=None):
    # Asegurarse de que la carpeta de salida exista
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Obtener la lista de archivos
    files = [f for f in os.listdir(folder_path) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff'))]
    total_files = len(files)

    # Iterar sobre todos los archivos en la carpeta
    for i, filename in enumerate(files, start=1):
        input_path = os.path.join(folder_path, filename)
        output_path = os.path.join(output_folder, filename)
        
        try:
            compress_image(input_path, output_path, quality)
            print(f"Imagen comprimida: {filename}")
        except Exception as e:
            print(f"Error al comprimir {filename}: {e}")

        # Actualizar la barra de progreso
        if progress_var and progress_bar:
            progress_var.set(i)
            progress_bar.update()

# Función para abrir el perfil de Instagram
def abrir_instagram():
    webbrowser.open("https://www.instagram.com/fatyvillaph/")

def select_folder_and_compress():
    # Crear la ventana de progreso
    progress_window = tk.Toplevel()
    progress_window.title("Progreso")
    progress_window.geometry("300x100")
    progress_window.iconbitmap('imag.ico')  # Establecer el ícono de la ventana principal

    # Variables para la barra de progreso
    progress_var = tk.IntVar()
    progress_bar = ttk.Progressbar(progress_window, maximum=100, variable=progress_var)
    progress_bar.pack(pady=20, padx=20)

    # Abrir un cuadro de diálogo para seleccionar la carpeta
    folder_path = filedialog.askdirectory(title="Selecciona la carpeta con las imágenes, deben ser .jpg")
    
    if folder_path:
        output_folder = os.path.join(folder_path, "archivoscomprimidos")
        
        # Actualizar el máximo de la barra de progreso al número de archivos
        total_files = len([f for f in os.listdir(folder_path) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff'))])
        progress_bar.config(maximum=total_files)
        
        # Comprimir todas las imágenes en la carpeta seleccionada
        compress_images_in_folder(folder_path, output_folder, quality=60, progress_var=progress_var, progress_bar=progress_bar)
        progress_window.destroy()

        # Mostrar mensaje y abrir perfil de Instagram al aceptar
        if messagebox.showinfo("Éxito", f"Todas las imágenes han sido comprimidas y guardadas en {output_folder}.\nSi este programa te sirve, ¡puedes hacerme saber en @fatyvillaph en Instagram!"):
            abrir_instagram()
    else:
        messagebox.showwarning("Cancelado", "No se seleccionó ninguna carpeta.")

# Crear la ventana principal de tkinter
root = tk.Tk()
root.withdraw()  # Oculta la ventana principal
root.iconbitmap('imag.ico')  # Establecer el ícono de la ventana principal
root.title("Compresor de Imágenes")

# Llamar a la función para seleccionar la carpeta y comprimir las imágenes
select_folder_and_compress()
