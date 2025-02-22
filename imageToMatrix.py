import cv2
import numpy as np
import csv

def color_distance(c1, c2):
    return np.sqrt(np.sum((c1 - c2) ** 2))

def encontrar_centroide(maze_matrix, valor):
    posiciones = np.argwhere(maze_matrix == valor)
    if len(posiciones) == 0:
        return None
    centroide = np.mean(posiciones, axis=0).astype(int)
    return tuple(centroide)

def discretize_image(image_path, grid_size=10, output_csv="maze_matrix.csv"):
    img = cv2.imread(image_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    height, width, _ = img.shape

    rows, cols = height // grid_size, width // grid_size
    maze_matrix = np.zeros((rows, cols), dtype=str)

    COLOR_ROJO = np.array([255, 0, 0])
    COLOR_VERDE = np.array([0, 255, 0])
    COLOR_NEGRO = np.array([0, 0, 0])
    COLOR_BLANCO = np.array([255, 255, 255])
    TOLERANCIA = 50

    for i in range(rows):
        for j in range(cols):
            block = img[i * grid_size:(i + 1) * grid_size, j * grid_size:(j + 1) * grid_size]
            avg_color = np.mean(block, axis=(0, 1))

            if color_distance(avg_color, COLOR_ROJO) < TOLERANCIA:
                maze_matrix[i, j] = '2'
            elif color_distance(avg_color, COLOR_VERDE) < TOLERANCIA:
                maze_matrix[i, j] = '3'
            elif color_distance(avg_color, COLOR_NEGRO) < TOLERANCIA:
                maze_matrix[i, j] = '1'
            elif color_distance(avg_color, COLOR_BLANCO) < TOLERANCIA:
                maze_matrix[i, j] = '0'
            else:
                maze_matrix[i, j] = '0'

    # para solo el inicio rojio
    inicio = encontrar_centroide(maze_matrix, '2')
    if inicio:
        maze_matrix[maze_matrix == '2'] = '0'
        maze_matrix[inicio[0], inicio[1]] = '2'

    # Guardar en CSV
    with open(output_csv, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(maze_matrix)

    for row in maze_matrix:
        print(" ".join(row))

    return maze_matrix

# Ejemplo de uso
#matrix = discretize_image("images/Prueba Lab1.bmp", grid_size=5)
#print(matrix)