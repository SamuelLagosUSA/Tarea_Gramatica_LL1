EPS = "ε"
FIN = "$"
SIMBOLO_INICIAL = "Programa"

PRODUCCIONES = [
    (1,  "Programa",  ["ListaSent"]),
    (2,  "ListaSent", ["Sent", "ListaSent"]),
    (3,  "ListaSent", []),
    (4,  "Sent",      ["id", "=", "Expr", ";"]),
    (5,  "Sent",      ["print", "Expr", ";"]),
    (6,  "Expr",      ["Term", "ExprP"]),
    (7,  "ExprP",     ["+", "Term", "ExprP"]),
    (8,  "ExprP",     ["-", "Term", "ExprP"]),
    (9,  "ExprP",     []),
    (10, "Term",      ["Factor", "TermP"]),
    (11, "TermP",     ["*", "Factor", "TermP"]),
    (12, "TermP",     ["/", "Factor", "TermP"]),
    (13, "TermP",     ["%", "Factor", "TermP"]),
    (14, "TermP",     []),
    (15, "Factor",    ["-", "Factor"]),
    (16, "Factor",    ["Primario"]),
    (17, "Primario",  ["num"]),
    (18, "Primario",  ["id"]),
    (19, "Primario",  ["(", "Expr", ")"]),
    (20, "Primario",  ["Func", "(", "Expr", ")"]),
    (21, "Func",      ["abs"]),
    (22, "Func",      ["sin"]),
    (23, "Func",      ["cos"]),
    (24, "Func",      ["tan"]),
]

NO_TERMINALES = ["Programa", "ListaSent", "Sent", "Expr", "ExprP",
                 "Term", "TermP", "Factor", "Primario", "Func"]

TERMINALES = ["id", "num", "print", "abs", "sin", "cos", "tan",
              "+", "-", "*", "/", "%", "=", ";", "(", ")"]


def texto_produccion(prod):
    num, izq, der = prod
    if len(der) == 0:
        return izq + " → " + EPS
    return izq + " → " + " ".join(der)



def primeros_de_secuencia(secuencia, primeros):
    """PRIMEROS de una lista de símbolos (ej: ['Term', 'ExprP'])."""
    resultado = set()
    for simbolo in secuencia:
        resultado = resultado | (primeros[simbolo] - {EPS})
        if EPS not in primeros[simbolo]:
            return resultado        
    resultado.add(EPS)               
    return resultado


def calcular_primeros():
    primeros = {}
    for t in TERMINALES:
        primeros[t] = {t}
    for nt in NO_TERMINALES:
        primeros[nt] = set()

    hubo_cambio = True
    while hubo_cambio:
        hubo_cambio = False
        for (num, izq, der) in PRODUCCIONES:
            nuevo = primeros_de_secuencia(der, primeros)
            if not nuevo.issubset(primeros[izq]):
                primeros[izq] = primeros[izq] | nuevo
                hubo_cambio = True
    return primeros


def calcular_siguientes(primeros):
    siguientes = {}
    for nt in NO_TERMINALES:
        siguientes[nt] = set()
    siguientes[SIMBOLO_INICIAL].add(FIN)

    hubo_cambio = True
    while hubo_cambio:
        hubo_cambio = False
        for (num, izq, der) in PRODUCCIONES:
            for i in range(len(der)):
                simbolo = der[i]
                if simbolo in NO_TERMINALES:
                    resto = der[i + 1:]         
                    f = primeros_de_secuencia(resto, primeros)
                    nuevo = f - {EPS}
                    if EPS in f:
                        nuevo = nuevo | siguientes[izq]
                    if not nuevo.issubset(siguientes[simbolo]):
                        siguientes[simbolo] = siguientes[simbolo] | nuevo
                        hubo_cambio = True
    return siguientes


def calcular_prediccion(primeros, siguientes):
    prediccion = {}
    for (num, izq, der) in PRODUCCIONES:
        f = primeros_de_secuencia(der, primeros)
        pred = f - {EPS}
        if EPS in f:
            pred = pred | siguientes[izq]
        prediccion[num] = pred
    return prediccion


def construir_tabla(prediccion):
    tabla = {}        
    conflictos = []
    for prod in PRODUCCIONES:
        num, izq, der = prod
        for terminal in prediccion[num]:
            clave = (izq, terminal)
            if clave in tabla:
                conflictos.append("Conflicto en M[" + izq + ", " + terminal
                                  + "]: producciones " + str(tabla[clave][0])
                                  + " y " + str(num))
            else:
                tabla[clave] = prod
    return tabla, conflictos

def conjunto_a_texto(conjunto):
    return "{ " + ", ".join(sorted(conjunto)) + " }"


def imprimir_gramatica():
    print("=== GRAMÁTICA ===")
    for prod in PRODUCCIONES:
        print("(" + str(prod[0]).rjust(2) + ") " + texto_produccion(prod))
    print()


def imprimir_primeros(primeros):
    print("=== PRIMEROS ===")
    for nt in NO_TERMINALES:
        print("PRIMEROS(" + nt + ") = " + conjunto_a_texto(primeros[nt]))
    print()


def imprimir_siguientes(siguientes):
    print("=== SIGUIENTES ===")
    for nt in NO_TERMINALES:
        print("SIGUIENTES(" + nt + ") = " + conjunto_a_texto(siguientes[nt]))
    print()


def imprimir_prediccion(prediccion):
    print("=== PREDICCIÓN ===")
    for prod in PRODUCCIONES:
        num = prod[0]
        texto = texto_produccion(prod)
        print("PRED(" + str(num).rjust(2) + ") " + texto.ljust(30)
              + " = " + conjunto_a_texto(prediccion[num]))
    print()


def imprimir_tabla(tabla, conflictos):
    print("=== TABLA LL(1) ===")
    for nt in NO_TERMINALES:
        for terminal in TERMINALES + [FIN]:
            if (nt, terminal) in tabla:
                prod = tabla[(nt, terminal)]
                print("M[" + nt + ", " + terminal + "] = ("
                      + str(prod[0]) + ") " + texto_produccion(prod))
    print()
    if len(conflictos) == 0:
        print("La gramática ES LL(1): no hay conflictos en la tabla.")
    else:
        print("La gramática NO es LL(1):")
        for c in conflictos:
            print("  " + c)
    print()
