from arbolabb.node import NodoABB
from arbolavl.node import NodoAVL
"""Operaciones ABB y AVL"""
def inorder_tree_walk(x, lista=None):
    if lista is None:
        lista = []
    if x is not None:
        inorder_tree_walk(x.left, lista)
        lista.append(x)
        inorder_tree_walk(x.right, lista)
    return lista

def preorder_tree_walk(x, lista=None):
    if lista is None:
        lista = []
    if x is not None:
        lista.append(x)
        preorder_tree_walk(x.left, lista)
        preorder_tree_walk(x.right, lista)
    return lista

def postorder_tree_walk(x, lista=None):
    if lista is None:
        lista = []
    if x is not None:
        postorder_tree_walk(x.left, lista)
        postorder_tree_walk(x.right, lista)
        lista.append(x)
    return lista

def iterative_tree_search(x, k):
    while x is not None and k != x.key:
        if k < x.key: x = x.left
        else: x = x.right
    return x

def tree_minimum(x):
    if x is None: return None
    while x.left is not None: x = x.left
    return x

def tree_maximum(x):
    if x is None: return None
    while x.right is not None: x = x.right
    return x

def tree_successor(x):
    if x is None: return None
    if x.right is not None: return tree_minimum(x.right)
    y = x.p
    while y is not None and x == y.right:
        x = y
        y = y.p
    return y

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


"""Operaciones usadas en ABB"""
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

    z = NodoABB(key, registro)
    z.p = y
    if y is None: T.root = z
    elif z.key < y.key: y.left = z
    else: y.right = z

    T.total_nodos += 1
    T.total_registros += 1
    return z

def tree_delete(T, z, tree_id=None):
    if z is None: return
    if tree_id is not None and len(z.registros) > 1:
        z.registros = [r for r in z.registros if r['tree_id'] != tree_id]
        T.total_registros -= 1
        return

    T.total_registros -= len(z.registros)
    T.total_nodos -= 1

    if z.left is None: transplant(T, z, z.right)
    elif z.right is None: transplant(T, z, z.left)
    else:
        y = tree_minimum(z.right)
        if y.p != z:
            transplant(T, y, y.right)
            y.right = z.right
            y.right.p = y
        transplant(T, z, y)
        y.left = z.left
        y.left.p = y

def calcular_altura_abb(root):
    if root is None: return -1
    nivel, altura = [root], -1
    while nivel:
        altura += 1
        sig = []
        for n in nivel:
            if n.left: sig.append(n.left)
            if n.right: sig.append(n.right)
        nivel = sig
    return altura