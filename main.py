from imageToMatrix import discretize_image
from maze_solver import Maze, GraphSearch
import matplotlib.pyplot as plt
import numpy as np
import csv

# Lista de diccionarios con el nombre del archivo y el tamaño del grid
files = [
    {"name": "Prueba Lab1.bmp", "grid_size": 10},
    {"name": "Test.bmp", "grid_size": 10},
    {"name": "Test2.bmp", "grid_size": 10},
    {"name": "turing.bmp", "grid_size": 5}
]

option = ""

while option != "6":
    print("\nBienvenido. Selecciona el número del laberinto que deseas probar:")
    for i, file in enumerate(files):
        print(f"{i + 1}. {file['name']} (Grid Size: {file['grid_size']})")
    print("5. Cargar archivo personalizado")
    print("6. Salir")
    
    option = input("Ingresa tu opción: ").strip()

    # Verificar si la opción es válida
    if option in [file["name"] for file in files]:
        # Obtener el archivo seleccionado
        selected_file = next(file for file in files if file["name"] == option)
        print(f"Opción válida discretizando: {selected_file['name']} con Grid Size: {selected_file['grid_size']}")

        # Discretizar la imagen
        path = "images/" + selected_file["name"]
        discretize_image(path, grid_size=selected_file["grid_size"])

        # Cargar el laberinto
        maze = Maze("maze_matrix.csv")

        # Crear una instancia de GraphSearch
        solver = GraphSearch(maze)

        # Ejecutar los algoritmos
        solver_option = ""
        while solver_option != "5":
            print("\nElige el tipo de solver:")
            print("1. BFS")
            print("2. DFS")
            print("3. A* (Manhattan)")
            print("4. A* (Euclidean)")
            print("5. Volver al menú principal")

            solver_option = input()

            path = []
            if solver_option == "1":
                print("Ejecutando BFS...")
                path = solver.bfs()
                print("BFS Path:", path)

            elif solver_option == "2":
                print("Ejecutando DFS...")
                path = solver.dfs()
                print("DFS Path:", path)
                
            elif solver_option == "3":
                print("Ejecutando A* (Manhattan)...")
                path = solver.a_star("manhattan")
                print("A* (Manhattan) Path:", path)

            elif solver_option == "4":
                print("Ejecutando A* (Euclidean)...")
                path = solver.a_star("euclidean")
                print("A* (Euclidean) Path:", path)

            elif solver_option == "5":
                print("Volviendo al menú principal...")
            else:
                print("Opción no válida. Intenta de nuevo.")

            if path:
                print("Mostrando el resultado.")

                # Asumimos que maze.matrix es una matriz 2D con los valores '0', '1', '2' y '3'
                rows = len(maze.matrix)
                cols = len(maze.matrix[0])
                
                # Creamos una imagen RGB donde asignamos un color a cada tipo de celda:
                # '0' -> blanco (camino libre), '1' -> negro (pared), 
                # '2' -> rojo (inicio) y '3' -> verde (meta)
                color_img = np.zeros((rows, cols, 3), dtype=np.uint8)
                for i in range(rows):
                    for j in range(cols):
                        if maze.matrix[i][j] == '0':
                            color_img[i, j] = [255, 255, 255]   # blanco
                        elif maze.matrix[i][j] == '1':
                            color_img[i, j] = [0, 0, 0]           # negro
                        elif maze.matrix[i][j] == '2':
                            color_img[i, j] = [255, 0, 0]         # rojo (inicio)
                        elif maze.matrix[i][j] == '3':
                            color_img[i, j] = [0, 255, 0]         # verde (meta)
                
                # Recorrer el path y marcar cada celda con color morado (por ejemplo: RGB [128, 0, 128])
                for (i, j) in path:
                    color_img[i, j] = [128, 0, 128]

                # Mostrar la imagen con matplotlib
                plt.figure(figsize=(8, 8))
                plt.imshow(color_img)
                plt.title("Laberinto con camino (morado)")
                plt.axis('off')
                plt.show()
