from imageToMatrix import discretize_image
from maze_solver import Maze, GraphSearch

# Lista de diccionarios con el nombre del archivo y el tamaño del grid
files = [
    {"name": "Prueba Lab1.bmp", "grid_size": 10},
    {"name": "Test.bmp", "grid_size": 10},
    {"name": "Test2.bmp", "grid_size": 10},
    {"name": "turing.bmp", "grid_size": 5}
]

option = ""

while option != "5":
    print("Bienvenido escribe el nombre del archivo que deseas probar o 5 para salir")
    
    for i in range(len(files)):
        print(f"{i + 1}. {files[i]['name']} (Grid Size: {files[i]['grid_size']})")
    print("5. Salir")

    option = input()

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

            
            # Nelson aqui podes poner tu parte, el path es una lista the tuplas (x,y). del objeto que se llama maze en este archivo
            # usa maze.matrix par obtener la matriz, se me ocurre que podes usar maze.matrix y la variable path para hacer un csv de resultado
            # y luego usar matplotlib para mostrar dicho csv donde esta el mapa con el path
            # en el lab le pusieron morado
            if path:
                print("Mostrando el resultado.")
                # :)
