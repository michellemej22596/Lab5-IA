import csv
import heapq
from collections import deque
# un poco de tipado para que sea un cachito mas lejible
from typing import List, Tuple, Optional

class Maze:
    def __init__(self, csv_file):
        self.matrix = self.load_csv(csv_file)
        self.rows = len(self.matrix)
        self.cols = len(self.matrix[0])
        self.start = self.find_position('2')  # Punto de inicio
        self.goals = self.find_positions('3')  # Posibles metas
        self.moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Arriba, Abajo, Izquierda, Derecha

    def load_csv(self, csv_file):
        """Carga la matriz desde un archivo CSV."""
        with open(csv_file, newline='') as f:
            reader = csv.reader(f)
            return [row for row in reader]

    def find_position(self, value):
        """Encuentra una única posición en la matriz."""
        for i in range(self.rows):
            for j in range(self.cols):
                if self.matrix[i][j] == value:
                    return (i, j)
        return None
    
    def find_positions(self, value):
        """Encuentra todas las posiciones de un valor en la matriz."""
        positions = []
        for i in range(self.rows):
            for j in range(self.cols):
                if self.matrix[i][j] == value:
                    positions.append((i, j))
        return positions

    def actions(self, s):
        """Devuelve las acciones posibles desde el estado s."""
        # s tiene la forma de tupla (x,y)
        x, y = s
        posibles_acciones = []

        # se itera en la lista de tuplas (posibples movimientos)
        for dx, dy in self.moves:
            
            nx, ny = x + dx, y + dy

            # las primeras 2 condiciones es para evitar los casos out of bounds de la matriz.

            # la tercera condicion es para ver que no sea una pared.
            if 0 <= nx < self.rows and 0 <= ny < self.cols and self.matrix[nx][ny] != '1':
                posibles_acciones.append((dx, dy))

        return posibles_acciones

    def cost(self, s, a, s_prime):
        """Devuelve el costo de moverse de s a s' con la acción a."""
        # por temas de simplicidad y que el laberitno es igual en todas las direcciones colocamos costo constante.
        return 1 

    def results(self, s, a):
        """Devuelve el nuevo estado después de aplicar la acción a en s."""
        x, y = s
        dx, dy = a
        return (x + dx, y + dy)

    def goalTest(self, s):
        """Verifica si el estado s es una meta."""
        return s in self.goals

class GraphSearch:
    def __init__(self, maze:Maze):
        self.maze = maze        

    def bfs(self) -> Optional[List[Tuple[int, int]]]:
        """Implementación de BFS (búsqueda en anchura)."""
        queue = deque([(self.maze.start, [])])
        visited = set()

        while queue:
            (node, path) = queue.popleft()
            if node in visited:
                continue
            visited.add(node)
            path = path + [node]

            if node in self.maze.goals:
                return path  # Camino encontrado

            for action in self.maze.actions(node):
                neighbor = self.maze.results(node, action)
                queue.append((neighbor, path))

        return None  # No se encontró camino

    def dfs(self) -> Optional[List[Tuple[int, int]]]:
        """Implementación de DFS (búsqueda en profundidad)."""
        stack = [(self.maze.start, [])]
        visited = set()

        while stack:
            (node, path) = stack.pop()
            if node in visited:
                continue
            visited.add(node)
            path = path + [node]

            if node in self.maze.goals:
                return path

            for action in self.maze.actions(node):
                neighbor = self.maze.results(node, action)
                stack.append((neighbor, path))


        return None

    def a_star(self, heuristic="manhattan") -> Optional[List[Tuple[int, int]]]:
        """Implementación de A* con heurísticas Manhattan o Euclidiana."""
        def manhattan(a, b):
            return abs(a[0] - b[0]) + abs(a[1] - b[1])

        def euclidean(a, b):
            return ((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2) ** 0.5

        heuristic_func = manhattan if heuristic == "manhattan" else euclidean

        open_set = []
        heapq.heappush(open_set, (0, self.maze.start, []))
        g_costs = {self.maze.start: 0}
        visited = set()

        while open_set:
            _, node, path = heapq.heappop(open_set)
            if node in visited:
                continue
            visited.add(node)
            path = path + [node]

            if node in self.maze.goals:
                return path  # Camino encontrado

            for action in self.maze.actions(node):
                neighbor = self.maze.results(node, action)
                new_cost = g_costs[node] + self.maze.cost(node, action, neighbor)
                if neighbor not in g_costs or new_cost < g_costs[neighbor]:
                    g_costs[neighbor] = new_cost
                    priority = new_cost + min(heuristic_func(neighbor, goal) for goal in self.maze.goals)
                    heapq.heappush(open_set, (priority, neighbor, path))

        return None  # No se encontró camino

# Todas las busquedas regresan una lista de tuplas con enteros, practicamente el camino, lista de coordenadas x,y

        # Se han elegido dos heurísticas distintas para A*:
        # 1. Heurística de Manhattan: Se usa porque en este laberinto solo se permiten movimientos ortogonales 
        #    (arriba, abajo, izquierda, derecha). Es eficiente y garantiza una buena estimación del costo restante.
        # 2. Heurística Euclidiana: Aunque suele usarse en espacios donde se permiten movimientos diagonales, 
        #    se incluye para comparar su desempeño en este problema, observando cómo afecta la expansión de nodos
        #    en un entorno con restricciones de movimiento.
