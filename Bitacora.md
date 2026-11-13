# BITACORA

*(Antes que todo se tuvo que comprimir el archivo Excel porque pesaba demasiado para poder subirlo directamente a GitHub)*

---

### Brandon
Realicé la configuración inicial del repositorio y la estructura de carpetas del proyecto, creando e implementé los archivos `node.py` y `tree.py` del árbol AVL en las carpetas `arbolabb/` y `arbolavl/`, como los que anteriormente hemos estado viendo para asegurar un rendimiento eficiente en las consultas. Programé la primera sección del archivo de operaciones (líneas 1 a 125).

### Daniel
Me hice cargo de la continuación del módulo de operaciones (`operaciones.py` de la línea 126 a la 261). Desarrollé las funciones de búsqueda optimizada, los algoritmos de recorridos y extracción de nodos (como en orden o por niveles) para listar los registros, y armé las rutinas de filtrado multicriterio para calcular las estadísticas poblacionales y métricas del arbolado urbano.

### OMAR
Armé la primera parte de la interfaz principal en el archivo `main.py` (de la línea 1 a la 189). Me enfoqué en estructurar el menú interactivo en la consola para que la navegación fuera fluida, controlando los estados y validando que las entradas del usuario no rompieran el programa. También me encargué de integrar y acomodar la base de datos dentro del repositorio para que el sistema pudiera leerla sin problemas.

### Fernanda
Continué con el desarrollo de la interfaz en `main.py` (de la línea 190 a la 351). Me tocó implementar los submenús de consulta avanzada, armar las vistas para los reportes analíticos que facilitan la toma de decisiones, y agregar todo el manejo de excepciones por si el usuario metía opciones o datos incorrectos.

# Peticiones LLM

**Qué se pidió** 

> Define las decisiones de diseño para resolver los problemas 1 al 4 del proyecto arbolado urbano  (elección de claves y política de claves duplicadas mediante encadenamiento). Proporciona el árbol de directorios exacto y la estructura completa de los archivos `node.py` y `tree.py` dentro de las carpetas `arbolabb/` y `arbolavl/`, asegurando que el nodo guarde el apuntador al padre `p` y la altura `h`, declarando las clases de forma explícita sin usar herencia.

**Qué respondió el LLM y se aceptó por el equipo:**

Para resolver los primeros 4 problemas del sistema, el diseño se apoya en las siguientes decisiones fundamentales:

1. **Elección de claves por estructura:**

   * Para los **Problemas 1 y 2**, se utilizan dos instancias de ABB: una indexada por `tree_id` (para búsqueda exacta y baja) y otra indexada por `especie`, cuyo recorrido inorden lista las especies alfabéticamente sin usar `sorted()`.

   * Para el **Problema 3**, se utiliza un AVL indexado por `tree_id` para evitar la degeneración provocada por identificadores crecientes, garantizando un costo $\Theta(\log n)$.

   * Para el **Problema 4**, se emplea un AVL indexado por `diametro` para realizar consultas por rango, obtener extremos (mínimo/máximo) y el sucesor.

2. **Política de claves duplicadas (Encadenamiento):** Dado que múltiples árboles comparten la misma especie o diámetro, cada nodo almacena una lista `self.registros` donde se encadenan los ejemplares. Esto mantiene claves únicas por nodo, cumpliendo la restricción del AVL.

**Estructura de directorios del proyecto:**

```
Arbolado-Urbano/
├── arbolabb/
│   ├── node.py
│   └── tree.py
├── arbolavl/
│   ├── node.py
│   └── tree.py
├── export.zip
├── main.py
└── operaciones.py

```

**Código de `arbolabb/node.py`**

```
class NodoABB:
    def __init__(self, key, registro):
        self.key = key
        self.registros = [registro]
        self.left = None
        self.right = None
        self.p = None

```

**Código de `arbolabb/tree.py`**

```
class ABB:
    def __init__(self):
        self.root = None
        self.total_nodos = 0
        self.total_registros = 0

```

**Código de `arbolavl/node.py`**

```
class NodoAVL:
    def __init__(self, key, registro):
        self.key = key
        self.registros = [registro]
        self.left = None
        self.right = None
        self.p = None
        self.h = 0

```

**Código de `arbolavl/tree.py`**

```
class AVL:
    def __init__(self):
        self.root = None
        self.total_nodos = 0
        self.total_registros = 0
        self.rotaciones_realizadas = 0

```

## 

**Qué se pidió** 

> Diseña el archivo `operaciones.py` que centralice las operaciones del ABB y del AVL. Utiliza únicamente Python básico. No resuelvas toda la lógica matemática de las rotaciones ni la eliminación, pero dame el esqueleto con las condicionales base, los ciclos `while` de búsqueda/inserción y la estructura recursiva de los recorridos para que nosotros terminemos de rellenar la lógica. Ten en cuenta que los nodos AVL y ABB son clases independientes.

**Qué respondió** 

Entregó el andamiaje lógico en `operaciones.py`. El AVL reutilizará los recorridos, búsquedas y la rutina de trasplante del ABB, operando sobre las clases independientes.

**Esqueleto de `operaciones.py`**

```
from arbolabb.node import NodoABB
from arbolavl.node import NodoAVL

# --- Operaciones compartidas (ABB y AVL) ---
def inorder_tree_walk(x, lista=None):
    if lista is None:
        lista = []
    if x is not None:
        inorder_tree_walk(x.left, lista)
        lista.append(x)
        inorder_tree_walk(x.right, lista)
    return lista

def iterative_tree_search(x, k):
    while x is not None and k != x.key:
        if k < x.key: x = x.left
        else: x = x.right
    return x

def tree_minimum(x):
    if x is None: return None
    while x.left is not None: 
        x = x.left
    return x

def transplant(T, u, v):
    if u.p is None: T.root = v
    elif u == u.p.left: u.p.left = v
    else: u.p.right = v
    if v is not None: v.p = u.p

def verificar_invariante_abb(root):
    nodos = []
    inorder_tree_walk(root, nodos)
    for i in range(len(nodos) - 1):
        if nodos[i].key >= nodos[i + 1].key: return False
    return True

# --- Operaciones usadas en ABB ---
def tree_insert(T, key, registro):
    y = None
    x = T.root
    while x is not None:
        y = x
        if key == x.key:
            x.registros.append(registro)
            T.total_registros += 1
            return x
        elif key < x.key: x = x.left
        else: x = x.right

    # Instanciar el nodo e integrarlo con su padre 'y'
    z = NodoABB(key, registro)
    # [Lógica de enlaces z.p = y pendiente de implementar por el equipo]
    return z

def tree_delete(T, z, tree_id=None):
    if z is None: return
    # Si hay múltiples registros (encadenamiento), solo filtramos el tree_id
    if tree_id is not None and len(z.registros) > 1:
        z.registros = [r for r in z.registros if r['tree_id'] != tree_id]
        T.total_registros -= 1
        return

    # [Lógica de los 3 casos de eliminación con transplant pendiente de implementar por el equipo]

# --- Operaciones utilizadas en AVL ---
def altura(x):
    return -1 if x is None else x.h

def factor_balance(x):
    return 0 if x is None else altura(x.left) - altura(x.right)

def right_rotate(T, z):
    y = z.left
    # [Lógica de reasignación de punteros y actualización de alturas pendiente]
    T.rotaciones_realizadas += 1
    return y

def rebalancear_hacia_arriba(T, nodo):
    actual = nodo
    while actual is not None:
        padre = actual.p
        # Evaluar factor_balance(actual) e invocar rotaciones LL, RR, LR o RL
        # [Lógica condicional de balanceo pendiente de implementar]
        actual = padre

def avl_insert(T, key, registro):
    # [Lógica de inserción similar a ABB]
    z = NodoAVL(key, registro)
    # [Lógica de enlaces]
    rebalancear_hacia_arriba(T, z.p)
    return z

def verificar_invariante_avl(root):
    if not verificar_invariante_abb(root):
        return False, 'No cumple la propiedad BST del ABB'
    nodos = []
    inorder_tree_walk(root, nodos)
    for n in nodos:
        fb = factor_balance(n)
        if fb < -1 or fb > 1:
            return False, f'Factor de equilibrio fuera de rango en nodo {n.key}: fb={fb}'
    return True, 'OK'

```

**Qué se completó por el equipo:**
El equipo programó íntegramente la lógica algorítmica matemática interna de las inserciones, eliminaciones, enlaces de punteros y rotaciones en `operaciones.py` utilizando Python nativo.

## 

**Qué se pidió** 

> Genera el archivo `main.py`. Debe leer los datos usando el módulo `csv` filtrando 10 especies y un máximo de 8,000 árboles por especie. Implementa la construcción de las instancias ABB y AVL, y desarrolla todo el menú interactivo para resolver las consultas de especies, búsqueda/baja por `tree_id`, rango de diámetros, extremos/sucesor y demostración de recorridos.

**Qué respondió el LLM (Código Aceptado):**

Proporcionó la implementación completa del menú de control integrando la carga de datos (usando `Counter` para extraer las especies con más registros) y los llamados directos a los algoritmos de `operaciones.py`.

**Código de `main.py`**

```
import csv
import sys
import time
from collections import Counter

from arbolabb.tree import ABB
from arbolavl.tree import AVL
from operaciones import *

sys.setrecursionlimit(100000)

# Parámetros del subconjunto solicitado
LIMITE_ESPECIES = 10
ARBOLES_POR_ESPECIE = 8000


def cargar_datos_csv(ruta_csv, max_especies=LIMITE_ESPECIES, max_por_especie=ARBOLES_POR_ESPECIE):
    """
    Selecciona las 10 especies con mayor presencia en export.csv y carga
    exactamente hasta 8,000 árboles por cada una de esas 10 especies.
    """
    conteo_especies = Counter()
    with open(ruta_csv, mode='r', encoding='utf-8') as archivo:
        lector = csv.DictReader(archivo)
        for fila in lector:
            esp = (fila.get('spc_common') or fila.get('spc_latin') or '').strip()
            if esp:
                conteo_especies[esp] += 1

    # Elegir las 10 especies principales (para garantizar que alcancen los 8,000 árboles)
    especies_elegidas = {esp for esp, _ in conteo_especies.most_common(max_especies)}
    conteo_actual = {esp: 0 for esp in especies_elegidas}
    registros = []

    with open(ruta_csv, mode='r', encoding='utf-8') as archivo:
        lector = csv.DictReader(archivo)
        for fila in lector:
            esp = (fila.get('spc_common') or fila.get('spc_latin') or '').strip()
            if esp not in especies_elegidas:
                continue
            if conteo_actual[esp] >= max_por_especie:
                continue

            try:
                tree_id = int(fila['tree_id'])
            except (ValueError, KeyError):
                continue

            try:
                diametro = float(fila.get('tree_dbh') or fila.get('stump_diam') or 0.0)
            except ValueError:
                diametro = 0.0

            salud = (fila.get('health') or 'N/A').strip()
            estado = (fila.get('status') or 'N/A').strip()
            barrio = (fila.get('boroname') or fila.get('borough') or 'N/A').strip()

            registros.append({
                'tree_id': tree_id,
                'especie': esp,
                'diametro': diametro,
                'salud': salud,
                'estado': estado,
                'barrio': barrio
            })
            conteo_actual[esp] += 1

            # Si las 10 especies ya llegaron a 8,000 árboles cada una, detenemos la lectura
            if all(c >= max_por_especie for c in conteo_actual.values()):
                break

    return registros, conteo_actual


def mostrar_tabla_arboles(lista_arboles, limite=15):
    if not lista_arboles:
        print("  [!] No se encontraron registros.")
        return
    print(f"\n  {'ID Árbol':<10} | {'Especie':<28} | {'Diám (in)':<10} | {'Salud':<8} | {'Estado':<8} | {'Barrio'}")
    print("  " + "-" * 85)
    for a in lista_arboles[:limite]:
        print(f"  {a['tree_id']:<10} | {a['especie'][:28]:<28} | {a['diametro']:<10.1f} | {a['salud']:<8} | {a['estado']:<8} | {a['barrio']}")
    if len(lista_arboles) > limite:
        print(f"  ... y {len(lista_arboles) - limite} registros adicionales.")


def submenu_especies(abb_especie):
    """Lista las 10 especies en orden alfabético mediante INORDER-TREE-WALK y filtra resultados."""
    nodos_inorden = inorder_tree_walk(abb_especie.root)
    if not nodos_inorden:
        print("  [!] El árbol de especies está vacío.")
        return

    print("\n" + "=" * 68)
    print(" LAS 10 ESPECIES EN ORDEN ALFABÉTICO")
    print("=" * 68)
    for idx, nodo in enumerate(nodos_inorden, start=1):
        print(f"  {idx:>2}. {nodo.key:<35} -> {len(nodo.registros)} árboles")

    print("\nOpciones:")
    print("  [1-10]  Ingresa el número de la especie para ver sus estadísticas y ejemplares")
    print("  [Texto] Escribe el nombre exacto de la especie")
    print("  [0]     Volver al menú principal")
    eleccion = input("\nSelecciona una especie: ").strip()

    if eleccion == '0' or not eleccion:
        return

    if eleccion.isdigit():
        indice = int(eleccion) - 1
        if 0 <= indice < len(nodos_inorden):
            clave_buscada = nodos_inorden[indice].key
        else:
            print("  [!] Número fuera de rango (elige entre 1 y 10).")
            return
    else:
        clave_buscada = eleccion

    t0 = time.perf_counter()
    nodo = iterative_tree_search(abb_especie.root, clave_buscada)
    t1 = time.perf_counter()

    if nodo is None:
        print(f"\n  [!] No se encontró la especie '{clave_buscada}'.")
    else:
        ejemplares = nodo.registros
        diametros = [r['diametro'] for r in ejemplares]
        vivos = sum(1 for r in ejemplares if r['estado'].lower() == 'alive')
        print(f"\n>>> Resultados para '{nodo.key}' (Localizado en {(t1 - t0)*1e6:.2f} µs)")
        print(f"    Total de ejemplares cargados : {len(ejemplares)}")
        print(f"    Ejemplares vivos             : {vivos}")
        print(f"    Diámetro promedio            : {sum(diametros)/len(diametros):.2f} pulgadas")
        print(f"    Diámetro mínimo / máximo     : {min(diametros):.1f} in / {max(diametros):.1f} in")
        mostrar_tabla_arboles(ejemplares, limite=15)


def demostrar_recorridos(abb_especie, avl_diametro, abb_id, avl_id):
    """Muestra claramente los 3 recorridos (Inorden, Preorden y Postorden) y verificadores."""
    print("\n" + "=" * 72)
    print(" 1. DEMOSTRACIÓN DE LOS 3 RECORRIDOS SOBRE EL ABB DE LAS 10 ESPECIES")
    print("=" * 72)

    nodos_pre = preorder_tree_walk(abb_especie.root)
    nodos_in = inorder_tree_walk(abb_especie.root)
    nodos_post = postorder_tree_walk(abb_especie.root)

    print("\n  A) PREORDEN (Raíz -> Izquierdo -> Derecho):")
    for i, n in enumerate(nodos_pre, 1):
        tipo = "RAÍZ" if n.p is None else ("HOJA" if n.left is None and n.right is None else "INTERNO")
        print(f"     {i:>2}. {n.key:<32} ({len(n.registros)} árboles) [{tipo}]")

    print("\n  B) INORDEN (Izquierdo -> Raíz -> Derecho | Queda en orden alfabético):")
    for i, n in enumerate(nodos_in, 1):
        print(f"     {i:>2}. {n.key:<32} ({len(n.registros)} árboles)")

    print("\n  C) POSTORDEN (Izquierdo -> Derecho -> Raíz | Hojas antes que el padre):")
    for i, n in enumerate(nodos_post, 1):
        tipo = "RAÍZ AL FINAL" if n.p is None else ("HOJA" if n.left is None and n.right is None else "INTERNO")
        print(f"     {i:>2}. {n.key:<32} ({len(n.registros)} árboles) [{tipo}]")

    print("\n" + "=" * 72)
    print(" 2. DEMOSTRACIÓN DE LOS 3 RECORRIDOS SOBRE EL AVL DE DIÁMETROS (Nodos)")
    print("=" * 72)
    avl_pre = [n.key for n in preorder_tree_walk(avl_diametro.root)]
    avl_in = [n.key for n in inorder_tree_walk(avl_diametro.root)]
    avl_post = [n.key for n in postorder_tree_walk(avl_diametro.root)]

    print(f"  Total de diámetros distintos (nodos en el AVL): {len(avl_in)}")
    print(f"  Preorden  (primeros 10 nodos visitados): {avl_pre[:10]}")
    print(f"  Inorden   (primeros 10 nodos ordenados): {avl_in[:10]}")
    print(f"  Postorden (primeros 10 nodos visitados): {avl_post[:10]}")

    print("\n" + "=" * 72)
    print(" 3. ALTURAS Y VERIFICADORES AUTOMÁTICOS DE INVARIANTE")
    print("=" * 72)
    h_abb_esp = calcular_altura_abb(abb_especie.root)
    h_abb_id = calcular_altura_abb(abb_id.root)
    h_avl_id = altura(avl_id.root)
    h_avl_diam = altura(avl_diametro.root)

    ok_abb_esp = verificar_invariante_abb(abb_especie.root)
    ok_abb_id = verificar_invariante_abb(abb_id.root)
    ok_avl_id, _ = verificar_invariante_avl(avl_id.root)
    ok_avl_diam, _ = verificar_invariante_avl(avl_diametro.root)

    print(f"  ABB por Especie  -> Nodos: {abb_especie.total_nodos:<6} | Registros: {abb_especie.total_registros:<6} | Altura h = {h_abb_esp:<5} | Invariante: {ok_abb_esp}")
    print(f"  ABB por ID       -> Nodos: {abb_id.total_nodos:<6} | Registros: {abb_id.total_registros:<6} | Altura h = {h_abb_id:<5} | Invariante: {ok_abb_id}")
    print(f"  AVL por ID       -> Nodos: {avl_id.total_nodos:<6} | Registros: {avl_id.total_registros:<6} | Altura h = {h_avl_id:<5} | Invariante: {ok_avl_id} (Rotaciones: {avl_id.rotaciones_realizadas})")
    print(f"  AVL por Diámetro -> Nodos: {avl_diametro.total_nodos:<6} | Registros: {avl_diametro.total_registros:<6} | Altura h = {h_avl_diam:<5} | Invariante: {ok_avl_diam} (Rotaciones: {avl_diametro.rotaciones_realizadas})")


def main():
    ruta_csv = 'export.csv'
    print(f"Filtrando {LIMITE_ESPECIES} especies y hasta {ARBOLES_POR_ESPECIE} árboles por especie desde '{ruta_csv}'...")
    try:
        datos, resumen_especies = cargar_datos_csv(ruta_csv)
    except FileNotFoundError:
        print(f"[Error] No se encontró el archivo '{ruta_csv}' en el directorio actual.")
        return

    print(f"\n Subconjunto cargado exitosamente: {len(datos)} árboles en {len(resumen_especies)} especies:")
    for i, (esp, cant) in enumerate(resumen_especies.items(), 1):
        print(f"   {i:>2}. {esp:<32}: {cant} árboles")

    abb_id = ABB()
    abb_especie = ABB()
    avl_id = AVL()
    avl_diametro = AVL()

    print("\nConstruyendo estructuras...")
    t0 = time.perf_counter()
    for reg in datos:
        tree_insert(abb_especie, reg['especie'], reg)
        tree_insert(abb_id, reg['tree_id'], reg)
    t1 = time.perf_counter()

    t2 = time.perf_counter()
    for reg in datos:
        avl_insert(avl_id, reg['tree_id'], reg)
        avl_insert(avl_diametro, reg['diametro'], reg)
    t3 = time.perf_counter()

    print(f"  -> ABB construido en {t1 - t0:.4f} s")
    print(f"  -> AVL construido en {t3 - t2:.4f} s")

    while True:
        print("\n" + "=" * 72)
        print(" SISTEMA DE GESTIÓN DEL ARBOLADO URBANO (10 ESPECIES / 8,000 POR ESPECIE)")
        print("=" * 72)
        print(" 1. Menú de las 10 especies en orden alfabético y consulta")
        print(" 2. Localizar un árbol por tree_id ")
        print(" 3. Dar de baja un árbol por tree_id conservando el orden")
        print(" 4. Recuperar árboles por rango de diámetro [a, b] en pulgadas")
        print(" 5. Árbol de menor y mayor diámetro, y sucesor inmediato")
        print(" 6. Demostración de los 3 recorridos (Preorden, Inorden, Postorden) y Alturas")
        print(" 0. Salir")
        opcion = input("\nElige una opción: ").strip()

        if opcion == '1':
            submenu_especies(abb_especie)

        elif opcion == '2':
            entrada = input("Ingresa el tree_id a buscar: ").strip()
            if not entrada.isdigit():
                print("  [!] El ID debe ser un número entero.")
                continue
            tid = int(entrada)

            t_a0 = time.perf_counter()
            nodo_abb = iterative_tree_search(abb_id.root, tid)
            t_a1 = time.perf_counter()

            t_v0 = time.perf_counter()
            nodo_avl = iterative_tree_search(avl_id.root, tid)
            t_v1 = time.perf_counter()

            if nodo_abb is None:
                print(f"  [!] El tree_id {tid} no está dentro del subconjunto de 10 especies.")
            else:
                mostrar_tabla_arboles(nodo_abb.registros, limite=1)
                print(f"\n  Tiempo en ABB : {(t_a1 - t_a0)*1e6:.2f} µs")
                print(f"  Tiempo en AVL : {(t_v1 - t_v0)*1e6:.2f} µs (Altura del nodo en AVL: h={nodo_avl.h}, fb={factor_balance(nodo_avl)})")

        elif opcion == '3':
            entrada = input("Ingresa el tree_id del árbol a dar de baja: ").strip()
            if not entrada.isdigit():
                print("  [!] El ID debe ser un número entero.")
                continue
            tid = int(entrada)

            nodo_id_abb = iterative_tree_search(abb_id.root, tid)
            if nodo_id_abb is None:
                print(f"  [!] No existe el árbol con ID {tid} en el subconjunto.")
                continue

            reg_baja = nodo_id_abb.registros[0]
            esp_baja = reg_baja['especie']
            diam_baja = reg_baja['diametro']

            # Baja en ABB (ID y Especie)
            tree_delete(abb_id, nodo_id_abb, tree_id=tid)
            nodo_esp = iterative_tree_search(abb_especie.root, esp_baja)
            tree_delete(abb_especie, nodo_esp, tree_id=tid)

            # Baja en AVL (ID y Diámetro)
            nodo_id_avl = iterative_tree_search(avl_id.root, tid)
            avl_delete(avl_id, nodo_id_avl, tree_id=tid)
            nodo_diam_avl = iterative_tree_search(avl_diametro.root, diam_baja)
            avl_delete(avl_diametro, nodo_diam_avl, tree_id=tid)

            print(f"  [OK] Árbol ID {tid} ('{esp_baja}', {diam_baja} in) eliminado correctamente.")
            print(f"       Total de árboles activos restantes: {abb_id.total_registros}")

        elif opcion == '4':
            try:
                min_d = float(input("Diámetro mínimo (pulgadas): ").strip())
                max_d = float(input("Diámetro máximo (pulgadas): ").strip())
            except ValueError:
                print("  [!] Ingresa valores numéricos válidos.")
                continue

            t0 = time.perf_counter()
            en_rango = []
            buscar_rango_avl(avl_diametro.root, min_d, max_d, en_rango)
            t1 = time.perf_counter()

            print(f"\n>>> Se recuperaron {len(en_rango)} árboles en el rango [{min_d}, {max_d}] in ({(t1 - t0)*1e3:.2f} ms):")
            mostrar_tabla_arboles(en_rango, limite=15)

        elif opcion == '5':
            nodo_min = tree_minimum(avl_diametro.root)
            nodo_max = tree_maximum(avl_diametro.root)
            if nodo_min is None or nodo_max is None:
                print("  [!] El AVL está vacío.")
                continue

            print(f"\n>>> MENOR DIÁMETRO ({nodo_min.key} in) -> {len(nodo_min.registros)} ejemplar(es):")
            mostrar_tabla_arboles(nodo_min.registros, limite=3)

            print(f"\n>>> MAYOR DIÁMETRO ({nodo_max.key} in) -> {len(nodo_max.registros)} ejemplar(es):")
            mostrar_tabla_arboles(nodo_max.registros, limite=3)

            entrada = input("\nIngresa un diámetro en pulgadas para obtener su SUCESOR inmediato: ").strip()
            try:
                d_val = float(entrada)
            except ValueError:
                continue

            nodo_actual = iterative_tree_search(avl_diametro.root, d_val)
            if nodo_actual is None:
                print(f"  [!] No existe ningún árbol con diámetro exacto de {d_val} in.")
            else:
                suc = tree_successor(nodo_actual)
                if suc is None:
                    print(f"  [!] El diámetro {d_val} in es el máximo del árbol; no tiene sucesor.")
                else:
                    print(f"\n>>> SUCESOR INMEDIATO de {d_val} in es {suc.key} in ({len(suc.registros)} ejemplares):")
                    mostrar_tabla_arboles(suc.registros, limite=5)

        elif opcion == '6':
            demostrar_recorridos(abb_especie, avl_diametro, abb_id, avl_id)

        elif opcion == '0':
            print("Saliendo del programa...")
            break
        else:
            print("  [!] Opción no válida.")


if __name__ == "__main__":
    main()

```