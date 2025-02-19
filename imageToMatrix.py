import cv2
import numpy as np
import csv

def discretize_image(image_path, grid_size=10, output_csv="maze_matrix.csv"):
    """
    Convierte una imagen de un laberinto en una matriz discreta y la guarda en un archivo CSV.
    :param image_path: Ruta de la imagen.
    :param grid_size: Tamaño del bloque a considerar por celda de la matriz.
    :param output_csv: Nombre del archivo CSV para guardar la matriz.
    :return: Matriz representando el laberinto.
    """
    # Cargar la imagen
    img = cv2.imread(image_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # Convertir de BGR a RGB
    height, width, _ = img.shape

    # Definir el tamaño de la matriz discreta
    rows, cols = height // grid_size, width // grid_size
    maze_matrix = np.zeros((rows, cols), dtype=str)

    # Iterar sobre la imagen en bloques de grid_size
    for i in range(rows):
        for j in range(cols):
            # Extraer el bloque de píxeles correspondiente
            block = img[i * grid_size:(i + 1) * grid_size, j * grid_size:(j + 1) * grid_size]

            # Calcular el color promedio
            avg_color = np.mean(block, axis=(0, 1))

            # Clasificar el color
            if np.all(avg_color < [50, 50, 50]):  # Negro -> Pared
                maze_matrix[i, j] = '1'
            elif np.all(avg_color > [200, 200, 200]):  # Blanco -> Camino libre
                maze_matrix[i, j] = '0'
            elif avg_color[0] > 150 and avg_color[1] < 100 and avg_color[2] < 100:  # Rojo -> Inicio
                maze_matrix[i, j] = '2'
            elif avg_color[1] > 150 and avg_color[0] < 100 and avg_color[2] < 100:  # Verde -> Meta
                maze_matrix[i, j] = '3'
            else:
                maze_matrix[i, j] = '0'  # Por defecto, camino libre

    # Guardar la matriz en un archivo CSV
    with open(output_csv, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(maze_matrix)

    # Imprimir la matriz
    for row in maze_matrix:
        print(" ".join(row))

    return maze_matrix

# Ejemplo de uso:
matrix = discretize_image("turing.bmp", grid_size=5)
#matrix = discretize_image("Test2.bmp", grid_size=5)
#matrix = discretize_image("Test.bmp", grid_size=5)
#matrix = discretize_image("Prueba Lab1.bmp", grid_size=5)
print(matrix)
