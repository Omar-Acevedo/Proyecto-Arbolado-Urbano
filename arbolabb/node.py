class NodoABB:
    def __init__(self, key, registro):
        self.key = key
        self.registros = [registro]
        self.left = None
        self.right = None
        self.p = None