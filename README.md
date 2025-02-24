# Proyecto: Resolución de Laberintos con Graph-Search

## Descripción General
Este proyecto tiene como objetivo resolver laberintos representados como imágenes mediante algoritmos de búsqueda en grafos. La imagen de entrada es discretizada en una matriz que representa el laberinto, y posteriormente, se aplican algoritmos de búsqueda para encontrar la solución.

## Estructura del Proyecto
El proyecto se divide en las siguientes tareas:

### **Task 1.1 - Discretización de la Imagen**
- Se convierte la imagen del laberinto en una matriz discreta donde:
  - `1` representa paredes (negro)
  - `0` representa caminos libres (blanco)
  - `2` representa el punto de inicio (rojo)
  - `3` representa la meta (verde)
- La segmentación se realiza automáticamente ajustando el tamaño de la cuadrícula en función de la resolución de la imagen.

### **Task 1.2 - Framework de Problemas**
- Se define una estructura orientada a objetos que encapsula el problema de la resolución del laberinto.
- Implementa funciones como:
  - `actions(s)`: posibles movimientos desde un estado
  - `stepCost(s, a, s')`: costo de transición entre estados
  - `goalTest(s)`: verifica si se ha alcanzado la meta

### **Task 1.3 - Algoritmos de Búsqueda**
Se implementan los siguientes algoritmos de búsqueda para encontrar la solución óptima del laberinto:
- **Breadth-First Search (BFS)**: Explora el laberinto en niveles, asegurando la solución más corta.
- **Depth-First Search (DFS)**: Explora caminos completos antes de retroceder, sin garantía de la ruta más corta.
- **A*** con dos heurísticas:
  - Distancia Manhattan
  - Distancia Euclidiana

### **Task 1.4 - Construcción de Salida**
- Se visualiza la solución encontrada sobre la matriz del laberinto.
- Se genera una representación gráfica mostrando el camino resuelto.

## Requisitos de Instalación
Para ejecutar el proyecto, se deben instalar las siguientes dependencias en Python:

```sh
pip install opencv-python numpy
```

---

## Video de la ejecución:

[![Watch the video](https://img.youtube.com/vi/IjdqCz4Nqqk/0.jpg)](https://youtu.be/IjdqCz4Nqqk)

