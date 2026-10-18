
import networkx as nx
import matplotlib.pyplot as plt
import heapq


def crear_grafo():
    """
    Construye un grafo dirigido.
    Cada arista representa un tramo y su peso es la distancia.
    """
    grafo = nx.DiGraph()

    conexiones = [
        ("A", "B", 4),
        ("A", "C", 2),
        ("B", "D", 5),
        ("B", "E", 10),
        ("C", "E", 3),
        ("D", "F", 3),
        ("E", "F", 4),
    ]

    grafo.add_weighted_edges_from(conexiones)
    return grafo


def dijkstra(grafo, inicio, meta):
    """
    Busca la ruta de menor costo desde inicio hasta meta.
    Devuelve la ruta encontrada y su costo total.
    """
    costos = {nodo: float("inf") for nodo in grafo.nodes}
    anteriores = {nodo: None for nodo in grafo.nodes}

    costos[inicio] = 0
    pendientes = [(0, inicio)]

    while pendientes:
        costo_actual, actual = heapq.heappop(pendientes)

        # Ignorar entradas que ya quedaron desactualizadas.
        if costo_actual > costos[actual]:
            continue

        # Detenerse cuando se extrae la meta con su costo mínimo.
        if actual == meta:
            break

        for vecino, datos in grafo[actual].items():
            nuevo_costo = (
                costo_actual + datos["weight"]
            )

            if nuevo_costo < costos[vecino]:
                costos[vecino] = nuevo_costo
                anteriores[vecino] = actual
                heapq.heappush(
                    pendientes, (nuevo_costo, vecino)
                )

    if costos[meta] == float("inf"):
        return None, float("inf")

    # Reconstruir la ruta desde la meta hacia el inicio.
    ruta = []
    actual = meta

    while actual is not None:
        ruta.append(actual)
        actual = anteriores[actual]

    ruta.reverse()
    return ruta, costos[meta]


def dibujar_grafo(grafo, ruta):
    """
    Dibuja el grafo y resalta la ruta óptima.
    """
    posiciones = {
        "A": (0, 1),
        "B": (1, 2),
        "C": (1, 0),
        "D": (2, 2),
        "E": (2, 0),
        "F": (3, 1),
    }

    plt.figure(figsize=(9, 5))

    nx.draw_networkx_nodes(
        grafo, posiciones, node_size=1100
    )
    nx.draw_networkx_labels(
        grafo, posiciones, font_size=12
    )
    nx.draw_networkx_edges(
        grafo, posiciones, edge_color="gray",
        arrows=True, arrowsize=20
    )

    etiquetas = nx.get_edge_attributes(
        grafo, "weight"
    )
    nx.draw_networkx_edge_labels(
        grafo, posiciones, edge_labels=etiquetas
    )

    if ruta:
        aristas_ruta = list(zip(ruta, ruta[1:]))
        nx.draw_networkx_edges(
            grafo, posiciones,
            edgelist=aristas_ruta,
            edge_color="red", width=3,
            arrows=True, arrowsize=22
        )

    plt.title("Ruta de menor costo con Dijkstra")
    plt.axis("off")
    plt.tight_layout()
    plt.show()


def main():
    """Ejecuta el problema completo."""
    grafo = crear_grafo()

    inicio = "A"
    meta = "F"

    ruta, costo = dijkstra(grafo, inicio, meta)

    if ruta is None:
        print("No existe una ruta hacia el destino.")
    else:
        print("Ruta óptima:", " -> ".join(ruta))
        print("Distancia total:", costo, "km")

    dibujar_grafo(grafo, ruta)


if __name__ == "__main__":
    main()
