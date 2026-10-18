
import heapq
import itertools
import matplotlib.pyplot as plt
import networkx as nx


# Cada fila es una lista de casillas.
# # = pared, S = inicio, G = meta, . = espacio libre.

LABERINTO = [
    "S..#....",
    ".#.#.##.",
    "...#....",
    "##...#..",
    "...#....",
    ".##.....",
    "....#..G",
]



def obtener_posicion(laberinto, simbolo):
    """
    Busca el símbolo indicado y devuelve su coordenada (fila, columna).
    """
    for fila, contenido in enumerate(laberinto):
        columna = contenido.find(simbolo)

        if columna != -1:
            return (fila, columna)

    raise ValueError(f"No se encontró el símbolo {simbolo}")


def es_transitable(laberinto, posicion):
    """
    Comprueba que la posición esté dentro de la cuadrícula
    y que no corresponda a una pared.
    """
    fila, columna = posicion

    return (
        0 <= fila < len(laberinto)
        and 0 <= columna < len(laberinto[0])
        and laberinto[fila][columna] != "#"
    )


def obtener_vecinos(laberinto, posicion):
    """
    Devuelve las casillas vecinas que se pueden visitar.
    Solo permite movimientos horizontales y verticales.
    """
    fila, columna = posicion

    movimientos = [
        (-1, 0),  # Arriba
        (1, 0),   # Abajo
        (0, -1),  # Izquierda
        (0, 1),   # Derecha
    ]

    vecinos = []

    for df, dc in movimientos:
        siguiente = (fila + df, columna + dc)

        if es_transitable(laberinto, siguiente):
            vecinos.append(siguiente)

    return vecinos


def heuristica(actual, meta):
    """
    Calcula la distancia Manhattan entre dos coordenadas.
    Es una estimación del costo que falta para llegar a la meta.
    """
    return (
        abs(actual[0] - meta[0])
        + abs(actual[1] - meta[1])
    )


def a_estrella(laberinto, inicio, meta):
    """
    Encuentra una ruta de costo mínimo mediante A*.
    Devuelve una lista de coordenadas o None si no hay solución.
    """
    contador = itertools.count()

    # La cola contiene: (f, orden, g, posición).
    pendientes = [
        (heuristica(inicio, meta), next(contador), 0, inicio)
    ]

    costos = {inicio: 0}
    anteriores = {inicio: None}

    while pendientes:
        _, _, costo_actual, actual = heapq.heappop(pendientes)

        # Ignorar entradas que ya no contienen el mejor costo.
        if costo_actual != costos.get(actual):
            continue

        if actual == meta:
            ruta = []
            actual_reconstruido = meta

            while actual_reconstruido is not None:
                ruta.append(actual_reconstruido)
                actual_reconstruido = anteriores[
                    actual_reconstruido
                ]

            ruta.reverse()
            return ruta

        for vecino in obtener_vecinos(laberinto, actual):
            nuevo_costo = costo_actual + 1

            if nuevo_costo < costos.get(
                vecino, float("inf")
            ):
                costos[vecino] = nuevo_costo
                anteriores[vecino] = actual

                prioridad = (
                    nuevo_costo + heuristica(vecino, meta)
                )

                heapq.heappush(
                    pendientes,
                    (
                        prioridad,
                        next(contador),
                        nuevo_costo,
                        vecino,
                    ),
                )

    return None


def dibujar_laberinto(laberinto, ruta):
    """
    Dibuja paredes, espacios, inicio, meta y ruta encontrada.
    También muestra el grafo de movimientos transitables.
    """
    filas = len(laberinto)
    columnas = len(laberinto[0])

    grafo = nx.grid_2d_graph(filas, columnas)

    # Eliminar los nodos que representan paredes.
    paredes = [
        (f, c)
        for f in range(filas)
        for c in range(columnas)
        if laberinto[f][c] == "#"
    ]

    grafo.remove_nodes_from(paredes)

    fig, ax = plt.subplots(figsize=(9, 7))

    # Dibujar la cuadrícula.
    ax.set_xlim(-0.5, columnas - 0.5)
    ax.set_ylim(filas - 0.5, -0.5)
    ax.set_xticks(range(columnas))
    ax.set_yticks(range(filas))
    ax.grid(True)
    ax.set_aspect("equal")

    # Colorear las paredes.
    for fila, columna in paredes:
        ax.add_patch(
            plt.Rectangle(
                (columna - 0.5, fila - 0.5),
                1, 1, color="gray"
            )
        )

    # Marcar la ruta si se encontró una solución.
    if ruta:
        x = [columna for fila, columna in ruta]
        y = [fila for fila, columna in ruta]

        ax.plot(
            x, y, marker="o", linewidth=3,
            label="Ruta A*"
        )

    inicio = obtener_posicion(laberinto, "S")
    meta = obtener_posicion(laberinto, "G")

    ax.scatter(
        inicio[1], inicio[0], s=180,
        marker="o", label="Inicio"
    )
    ax.scatter(
        meta[1], meta[0], s=180,
        marker="*", label="Meta"
    )

    ax.set_title("Resolución del laberinto con A*")
    ax.legend()
    plt.tight_layout()
    plt.show()


def main():
    """Coordina la búsqueda y la visualización."""
    inicio = obtener_posicion(LABERINTO, "S")
    meta = obtener_posicion(LABERINTO, "G")

    ruta = a_estrella(LABERINTO, inicio, meta)

    if ruta is None:
        print("No existe una ruta hacia la salida.")
    else:
        print("Ruta encontrada:")

        for posicion in ruta:
            print(posicion)

        print("Cantidad de movimientos:", len(ruta) - 1)

    dibujar_laberinto(LABERINTO, ruta)


if __name__ == "__main__":
    main()
