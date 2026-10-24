
import math
import random
import matplotlib.pyplot as plt

# Fijar semilla para facilitar la reproducibilidad.
random.seed(42)

# Coordenadas simuladas de los puntos de entrega.
puntos = {
    "Almacen": (0, 0),
    "A": (2, 6),
    "B": (5, 8),
    "C": (8, 3),
    "D": (6, 1),
    "E": (1, 3)
}

ALMACEN = "Almacen"
ENTREGAS = [p for p in puntos if p != ALMACEN]


def distancia(a, b):
    """Calcula la distancia euclidiana entre dos puntos."""
    x1, y1 = puntos[a]
    x2, y2 = puntos[b]
    return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)


def costo(ruta):
    """Suma las distancias de la ruta, incluido el regreso."""
    recorrido = [ALMACEN] + ruta + [ALMACEN]

    return sum(
        distancia(recorrido[i], recorrido[i + 1])
        for i in range(len(recorrido) - 1)
    )


def vecino(ruta):
    """Genera una ruta nueva intercambiando dos entregas."""
    nueva = ruta.copy()
    i, j = random.sample(range(len(nueva)), 2)
    nueva[i], nueva[j] = nueva[j], nueva[i]
    return nueva


def hill_climbing(iteraciones=1000):
    """Conserva solamente los movimientos que mejoran la ruta."""
    actual = random.sample(ENTREGAS, len(ENTREGAS))
    mejor_costo = costo(actual)
    historial = [mejor_costo]

    for _ in range(iteraciones):
        candidata = vecino(actual)
        costo_candidata = costo(candidata)

        if costo_candidata < mejor_costo:
            actual = candidata
            mejor_costo = costo_candidata

        historial.append(mejor_costo)

    return actual, mejor_costo, historial


def simulated_annealing(
    iteraciones=10000,
    temperatura_inicial=100,
    enfriamiento=0.995
):
    """Acepta algunas soluciones peores para escapar de óptimos locales."""
    actual = random.sample(ENTREGAS, len(ENTREGAS))
    costo_actual = costo(actual)

    mejor = actual.copy()
    mejor_costo = costo_actual
    historial = [mejor_costo]
    temperatura = temperatura_inicial

    for _ in range(iteraciones):
        candidata = vecino(actual)
        costo_candidata = costo(candidata)

        diferencia = costo_candidata - costo_actual

        # Aceptar mejoras o, con cierta probabilidad,
        # aceptar un movimiento que aumente el costo.
        if (
            diferencia < 0
            or random.random() < math.exp(
                -diferencia / temperatura
            )
        ):
            actual = candidata
            costo_actual = costo_candidata

        # Conservar siempre la mejor solución observada.
        if costo_actual < mejor_costo:
            mejor = actual.copy()
            mejor_costo = costo_actual

        historial.append(mejor_costo)
        temperatura *= enfriamiento

        # Evitar temperaturas demasiado cercanas a cero.
        temperatura = max(temperatura, 1e-10)

    return mejor, mejor_costo, historial


# Ejecutar los dos algoritmos.
ruta_hc, costo_hc, historial_hc = hill_climbing()
ruta_sa, costo_sa, historial_sa = simulated_annealing()

# Mostrar los resultados.
print("=== HILL CLIMBING ===")
print("Ruta:", " -> ".join(
    [ALMACEN] + ruta_hc + [ALMACEN]
))
print(f"Distancia total: {costo_hc:.2f}")

print("\n=== SIMULATED ANNEALING ===")
print("Ruta:", " -> ".join(
    [ALMACEN] + ruta_sa + [ALMACEN]
))
print(f"Distancia total: {costo_sa:.2f}")

if costo_sa < costo_hc:
    print("\nSimulated Annealing obtuvo una ruta más corta.")
elif costo_hc < costo_sa:
    print("\nHill Climbing obtuvo una ruta más corta.")
else:
    print("\nAmbos algoritmos obtuvieron el mismo costo.")

# Graficar la convergencia.
plt.figure(figsize=(10, 5))
plt.plot(
    historial_hc,
    label="Hill Climbing"
)
plt.plot(
    historial_sa,
    label="Simulated Annealing"
)

plt.xlabel("Iteraciones")
plt.ylabel("Mejor distancia encontrada")
plt.title("Comparación de convergencia")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("convergencia_busqueda_local.png", dpi=150)
plt.show()
