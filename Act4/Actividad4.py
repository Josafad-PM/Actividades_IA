
from collections import deque
from time import perf_counter


# Laberinto: # es pared, S es inicio y G es meta.
LABERINTO = [
    "##########",
    "#S...#...#",
    "#.#..#.#.#",
    "#.#....#.#",
    "#.####...#",
    "#......#G#",
    "##########"
]


def encontrar_posicion(simbolo):
    """Devuelve las coordenadas de S o G."""
    for fila, contenido in enumerate(LABERINTO):
        columna = contenido.find(simbolo)

        if columna != -1:
            return fila, columna

    raise ValueError(f"No se encontró {simbolo}")


INICIO = encontrar_posicion("S")
META = encontrar_posicion("G")


def obtener_vecinos(posicion):
    """Obtiene los vecinos transitables de una celda."""
    fila, columna = posicion

    movimientos = [
        (-1, 0),  # Arriba
        (1, 0),   # Abajo
        (0, -1),  # Izquierda
        (0, 1)    # Derecha
    ]

    vecinos = []

    for df, dc in movimientos:
        nf = fila + df
        nc = columna + dc

        dentro = (
            0 <= nf < len(LABERINTO)
            and 0 <= nc < len(LABERINTO[0])
        )

        if dentro and LABERINTO[nf][nc] != "#":
            vecinos.append((nf, nc))

    return vecinos


def reconstruir_ruta(padres, meta):
    """Reconstruye el camino desde la meta hasta el inicio."""
    ruta = []
    actual = meta

    while actual is not None:
        ruta.append(actual)
        actual = padres[actual]

    ruta.reverse()
    return ruta


def bfs(inicio, meta):
    """Busca por niveles usando una cola FIFO."""
    cola = deque([inicio])
    visitados = {inicio}
    padres = {inicio: None}
    expandidos = 0

    while cola:
        actual = cola.popleft()
        expandidos += 1

        if actual == meta:
            return reconstruir_ruta(padres, meta), expandidos

        for vecino in obtener_vecinos(actual):
            if vecino not in visitados:
                visitados.add(vecino)
                padres[vecino] = actual
                cola.append(vecino)

    return None, expandidos


def dfs(inicio, meta):
    """Busca profundizando en las ramas mediante una pila."""
    pila = [inicio]
    visitados = {inicio}
    padres = {inicio: None}
    expandidos = 0

    while pila:
        actual = pila.pop()
        expandidos += 1

        if actual == meta:
            return reconstruir_ruta(padres, meta), expandidos

        # El orden de vecinos determina qué rama se explora primero.
        for vecino in reversed(obtener_vecinos(actual)):
            if vecino not in visitados:
                visitados.add(vecino)
                padres[vecino] = actual
                pila.append(vecino)

    return None, expandidos


def mostrar_laberinto(ruta, nombre):
    """Dibuja la ruta con asteriscos."""
    mapa = [list(fila) for fila in LABERINTO]

    if ruta:
        for fila, columna in ruta:
            if mapa[fila][columna] not in ("S", "G"):
                mapa[fila][columna] = "*"

    print(f"\nLaberinto resuelto con {nombre}:")

    for fila in mapa:
        print("".join(fila))


def ejecutar(nombre, algoritmo):
    """Ejecuta el algoritmo y mide sus resultados."""
    inicio_tiempo = perf_counter()

    ruta, expandidos = algoritmo(INICIO, META)

    tiempo = perf_counter() - inicio_tiempo

    print(f"\n--- {nombre} ---")
    print("Inicio:", INICIO)
    print("Meta:", META)
    print("Nodos expandidos:", expandidos)
    print(f"Tiempo: {tiempo:.8f} segundos")

    if ruta:
        print("Ruta:", ruta)
        print("Número de movimientos:", len(ruta) - 1)
    else:
        print("No existe una ruta hasta la meta.")

    mostrar_laberinto(ruta, nombre)

    return ruta, expandidos, tiempo


if __name__ == "__main__":
    resultado_bfs = ejecutar("BFS", bfs)
    resultado_dfs = ejecutar("DFS", dfs)

    ruta_bfs, nodos_bfs, tiempo_bfs = resultado_bfs
    ruta_dfs, nodos_dfs, tiempo_dfs = resultado_dfs

    print("\n--- COMPARACIÓN FINAL ---")

    if ruta_bfs:
        print("Movimientos BFS:", len(ruta_bfs) - 1)

    if ruta_dfs:
        print("Movimientos DFS:", len(ruta_dfs) - 1)

    print("Nodos expandidos BFS:", nodos_bfs)
    print("Nodos expandidos DFS:", nodos_dfs)
    print(f"Tiempo BFS: {tiempo_bfs:.8f} s")
    print(f"Tiempo DFS: {tiempo_dfs:.8f} s")
