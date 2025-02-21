import csv
import heapq
from collections import deque

class MazeSolver:
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

    def get_neighbors(self, node):
        """Devuelve los vecinos válidos de un nodo."""
        neighbors = []
        x, y = node
        for dx, dy in self.moves:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.rows and 0 <= ny < self.cols and self.matrix[nx][ny] != '1':  # No es pared
                neighbors.append((nx, ny))
        return neighbors

    def bfs(self):
        """Implementación de BFS (búsqueda en anchura)."""
        queue = deque([(self.start, [])])
        visited = set()

        while queue:
            (node, path) = queue.popleft()
            if node in visited:
                continue
            visited.add(node)
            path = path + [node]

            if node in self.goals:
                return path  # Camino encontrado

            for neighbor in self.get_neighbors(node):
                queue.append((neighbor, path))

        return None  # No se encontró camino

    def dfs(self):
        """Implementación de DFS (búsqueda en profundidad)."""
        stack = [(self.start, [])]
        visited = set()

        while stack:
            (node, path) = stack.pop()
            if node in visited:
                continue
            visited.add(node)
            path = path + [node]

            if node in self.goals:
                return path

            for neighbor in self.get_neighbors(node):
                stack.append((neighbor, path))

        return None

    def a_star(self, heuristic="manhattan"):
        """Implementación de A* con heurísticas Manhattan o Euclidiana."""
        def manhattan(a, b):
            return abs(a[0] - b[0]) + abs(a[1] - b[1])

        def euclidean(a, b):
            return ((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2) ** 0.5

        heuristic_func = manhattan if heuristic == "manhattan" else euclidean

        open_set = []
        heapq.heappush(open_set, (0, self.start, []))
        g_costs = {self.start: 0}
        visited = set()

        while open_set:
            _, node, path = heapq.heappop(open_set)
            if node in visited:
                continue
            visited.add(node)
            path = path + [node]

            if node in self.goals:
                return path  # Camino encontrado

            for neighbor in self.get_neighbors(node):
                new_cost = g_costs[node] + 1
                if neighbor not in g_costs or new_cost < g_costs[neighbor]:
                    g_costs[neighbor] = new_cost
                    priority = new_cost + min(heuristic_func(neighbor, goal) for goal in self.goals)
                    heapq.heappush(open_set, (priority, neighbor, path))

        return None  # No se encontró camino


# **Ejecutar los algoritmos con el CSV**
if __name__ == "__main__":
    solver = MazeSolver("maze_matrix.csv")

    print("BFS Path:", solver.bfs())
    print("DFS Path:", solver.dfs())
    print("A* (Manhattan) Path:", solver.a_star("manhattan"))
    print("A* (Euclidean) Path:", solver.a_star("euclidean"))


        # Se han elegido dos heurísticas distintas para A*:
        # 1. Heurística de Manhattan: Se usa porque en este laberinto solo se permiten movimientos ortogonales 
        #    (arriba, abajo, izquierda, derecha). Es eficiente y garantiza una buena estimación del costo restante.
        # 2. Heurística Euclidiana: Aunque suele usarse en espacios donde se permiten movimientos diagonales, 
        #    se incluye para comparar su desempeño en este problema, observando cómo afecta la expansión de nodos
        #    en un entorno con restricciones de movimiento.
