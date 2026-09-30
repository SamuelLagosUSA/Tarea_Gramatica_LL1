from lex import tokenizar, ErrorLexico
from gramatica import (calcular_primeros, calcular_siguientes,
                       calcular_prediccion, construir_tabla,
                       imprimir_gramatica, imprimir_primeros,
                       imprimir_siguientes, imprimir_prediccion,
                       imprimir_tabla)
from parser_ll1 import parsear, imprimir_arbol, ErrorSintactico
from semantica import Semantica, ErrorSemantico

MOSTRAR_TOKENS = False
MOSTRAR_ARBOL = False
MOSTRAR_TRAZA = False


primeros = calcular_primeros()
siguientes = calcular_siguientes(primeros)
prediccion = calcular_prediccion(primeros, siguientes)
tabla, conflictos = construir_tabla(prediccion)


def procesar(texto, semantica):
    try:
      
        tokens = tokenizar(texto)
        if MOSTRAR_TOKENS:
            for t in tokens:
                print(t)

  
        arbol = parsear(tokens, tabla, MOSTRAR_TRAZA)
        if MOSTRAR_ARBOL:
            imprimir_arbol(arbol)

        
        semantica.ejecutar(arbol)

    except ErrorLexico as e:
        print("[Error léxico] " + str(e))
    except ErrorSintactico as e:
        print("[Error sintáctico] " + str(e))
    except ErrorSemantico as e:
        print("[Error semántico] " + str(e))


def modo_interactivo(semantica):
    print("Escribe sentencias terminadas en ';' (escribe 'salir' para volver)")
    print("Ejemplo: x = 3 + 4 * 2; print sin(x) + abs(-5);")
    while True:
        linea = input(">>> ")
        if linea.strip().lower() == "salir":
            break
        if linea.strip() != "":
            procesar(linea, semantica)


def modo_archivo(semantica):
    nombre = input("Nombre del archivo: ")
    try:
        archivo = open(nombre, "r", encoding="utf-8")
        texto = archivo.read()
        archivo.close()
    except FileNotFoundError:
        print("No se encontró el archivo.")
        return
    procesar(texto, semantica)


def main():
    if len(conflictos) > 0:
        print("La gramática no es LL(1):")
        for c in conflictos:
            print("  " + c)
        return

    semantica = Semantica()

    while True:
        print()
        print("===== INTÉRPRETE LL(1) =====")
        print("1. Mostrar gramática, PRIMEROS, SIGUIENTES, PREDICCIÓN y tabla")
        print("2. Modo interactivo")
        print("3. Ejecutar un archivo")
        print("0. Salir")
        opcion = input("Opción: ")

        if opcion == "1":
            imprimir_gramatica()
            imprimir_primeros(primeros)
            imprimir_siguientes(siguientes)
            imprimir_prediccion(prediccion)
            imprimir_tabla(tabla, conflictos)
        elif opcion == "2":
            modo_interactivo(semantica)
        elif opcion == "3":
            modo_archivo(semantica)
        elif opcion == "0":
            break
        else:
            print("Opción no válida.")


main()
