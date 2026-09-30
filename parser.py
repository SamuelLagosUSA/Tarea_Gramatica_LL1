from gramatica import TERMINALES, FIN, SIMBOLO_INICIAL


class ErrorSintactico(Exception):
    pass


class Nodo:
    """Nodo del árbol de derivación."""
    def __init__(self, simbolo):
        self.simbolo = simbolo
        self.token = None     
        self.hijos = []


def imprimir_arbol(nodo, nivel=0):
    texto = "    " * nivel + nodo.simbolo
    if nodo.token is not None:
        texto = texto + " [" + nodo.token.lexema + "]"
    print(texto)
    for hijo in nodo.hijos:
        imprimir_arbol(hijo, nivel + 1)
 
    if nodo.token is None and len(nodo.hijos) == 0:
        print("    " * (nivel + 1) + "ε")


def crear_error(token, esperados):
    if token.tipo == FIN:
        encontrado = "fin de entrada"
    else:
        encontrado = "'" + token.lexema + "'"
    return ErrorSintactico("Línea " + str(token.linea) + ", columna "
                           + str(token.columna) + ": se encontró "
                           + encontrado + "; se esperaba: "
                           + ", ".join(sorted(esperados)))


def parsear(tokens, tabla, mostrar_traza=False):
    raiz = Nodo(SIMBOLO_INICIAL)
    pila = [Nodo(FIN), raiz]     
    pos = 0

    if mostrar_traza:
        print("PILA".ljust(45) + "ENTRADA".ljust(35) + "ACCIÓN")

    while True:
        pila_txt = " ".join([n.simbolo for n in reversed(pila)])
        entrada_txt = " ".join([t.tipo for t in tokens[pos:]])

        tope = pila.pop()
        actual = tokens[pos]

        if tope.simbolo == FIN:
            if actual.tipo != FIN:
                raise crear_error(actual, [FIN])
            if mostrar_traza:
                print(pila_txt.ljust(45) + entrada_txt.ljust(35) + "ACEPTAR")
            return raiz

        if tope.simbolo in TERMINALES:
            if tope.simbolo != actual.tipo:
                raise crear_error(actual, [tope.simbolo])
            tope.token = actual
            pos = pos + 1
            accion = "match " + actual.tipo

        else:
            clave = (tope.simbolo, actual.tipo)
            if clave not in tabla:
                esperados = []
                for (nt, terminal) in tabla:
                    if nt == tope.simbolo:
                        esperados.append(terminal)
                raise crear_error(actual, esperados)

            produccion = tabla[clave]
            lado_derecho = produccion[2]

            hijos = []
            for simbolo in lado_derecho:
                hijos.append(Nodo(simbolo))
            tope.hijos = hijos
            for hijo in reversed(hijos):
                pila.append(hijo)

            accion = "(" + str(produccion[0]) + ") " + produccion[1] + " → "
            if len(lado_derecho) == 0:
                accion = accion + "ε"
            else:
                accion = accion + " ".join(lado_derecho)

        if mostrar_traza:
            print(pila_txt.ljust(45) + entrada_txt.ljust(35) + accion)
