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

    # Caso de laberintos predefinidos (opciones 1 a 4)
    if option in [str(i) for i in range(1, 5)]:
        selected_file = files[int(option) - 1]
        print(f"\nOpción válida: discretizando {selected_file['name']} con Grid Size: {selected_file['grid_size']}")
        path_to_file = "images/" + selected_file["name"]
        discretize_image(path_to_file, grid_size=selected_file["grid_size"])

    # Caso de archivo personalizado
    elif option == "5":
        file_path = input("Ingresa el nombre del archivo (con extensión y ruta si aplica): ").strip()
        grid_size_input = input("Ingresa el grid size: ").strip()
        try:
            grid_size_val = int(grid_size_input)
        except ValueError:
            print("Grid size inválido. Se usará 10 por defecto.")
            grid_size_val = 10
        discretize_image(file_path, grid_size=grid_size_val)

    elif option == "6":
        print("Saliendo...")
        break

    else:
        print("Opción no válida. Intenta de nuevo.")
        continue

    # Cargar el laberinto y crear el solver
    maze = Maze("maze_matrix.csv")
    solver = GraphSearch(maze)
    
    solver_option = ""
    while solver_option != "5":
        print("\nElige el tipo de solver:")
        print("1. BFS")
        print("2. DFS")
        print("3. A* (Manhattan)")
        print("4. A* (Euclidean)")
        print("5. Volver al menú principal")
        solver_option = input("Ingresa tu opción: ").strip()

        solution_path = []
        if solver_option == "1":
            print("Ejecutando BFS...")
            solution_path = solver.bfs()
            print("BFS Path:", solution_path)
        elif solver_option == "2":
            print("Ejecutando DFS...")
            solution_path = solver.dfs()
            print("DFS Path:", solution_path)
        elif solver_option == "3":
            print("Ejecutando A* (Manhattan)...")
            solution_path = solver.a_star("manhattan")
            print("A* (Manhattan) Path:", solution_path)
        elif solver_option == "4":
            print("Ejecutando A* (Euclidean)...")
            solution_path = solver.a_star("euclidean")
            print("A* (Euclidean) Path:", solution_path)
        elif solver_option == "5":
            print("Volviendo al menú principal...")
            break
        else:
            print("Opción no válida. Intenta de nuevo.")
            continue

        # Si se encontró una solución, se genera el CSV y la visualización
        if solution_path:
            print("Generando CSV y visualización de la solución...")

            # Crear copia de la matriz original para agregar la solución
            result_matrix = [row.copy() for row in maze.matrix]
            # Marcar el camino con 'P' (para indicar morado), excepto en el inicio y la meta
            for (i, j) in solution_path:
                if (i, j) == maze.start or (i, j) in maze.goals:
                    continue
                result_matrix[i][j] = 'P'

            # Guardar la matriz resultante en un CSV (por ejemplo, maze_solution.csv)
            with open("maze_solution.csv", "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerows(result_matrix)

            # Crear imagen RGB para visualizar la solución
            rows = len(maze.matrix)
            cols = len(maze.matrix[0])
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
            
            # Pintar el camino en morado, omitiendo el inicio y la meta
            for (i, j) in solution_path:
                if (i, j) == maze.start or (i, j) in maze.goals:
                    continue
                color_img[i, j] = [128, 0, 128]  # color morado

            plt.figure(figsize=(8, 8))
            plt.imshow(color_img)
            plt.title("Laberinto con solución (morado)")
            plt.axis("off")
            plt.show()
        else:
            print("No se encontró solución para este laberinto.")
