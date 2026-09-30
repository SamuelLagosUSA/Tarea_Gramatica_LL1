# Intérprete LL(1) en Python

Proyecto que implementa una gramática LL(1) para un lenguaje sencillo de expresiones aritméticas. Incluye análisis léxico, sintáctico y semántico.

## Qué hace

- Operaciones: `+`, `-`, `*`, `/`, `%`
- Funciones: `abs`, `sin`, `cos`, `tan` (las trigonométricas usan radianes)
- Asignación de variables: `x = 5;`
- Mostrar resultados con `print`: `print x + 2;`
- Constantes predefinidas: `pi` y `e`
- Comentarios con `#`
- Muestra los conjuntos PRIMEROS, SIGUIENTES, PREDICCIÓN y la tabla LL(1)

## Archivos

| Archivo | Para qué sirve |
|---|---|
| `lex.py` | Análisis léxico: convierte el texto en tokens |
| `gramatica.py` | Producciones, PRIMEROS, SIGUIENTES, PREDICCIÓN y tabla LL(1) |
| `parser_ll1.py` | Análisis sintáctico con pila y tabla. Construye el árbol |
| `semantica.py` | Análisis semántico: tabla de símbolos y evaluación |
| `main.py` | Menú principal del programa |

## Requisitos

- Python 3.6 o superior
- No necesita instalar librerías externas

## Cómo ejecutarlo

1. Guardar los 5 archivos `.py` en la misma carpeta.
2. Abrir una terminal en esa carpeta.
3. Ejecutar:

```bash
python main.py
```

(En algunos sistemas puede ser `python3 main.py`.)

## Menú

```
1. Mostrar gramática, PRIMEROS, SIGUIENTES, PREDICCIÓN y tabla
2. Modo interactivo
3. Ejecutar un archivo
0. Salir
```

- **Opción 1:** imprime la gramática y todos los conjuntos.
- **Opción 2:** se escriben sentencias una por una. Escribir `salir` para volver al menú.
- **Opción 3:** pide el nombre de un archivo de texto con un programa y lo ejecuta.

## Ejemplo de programa

```
x = 10 % 4 + 3 * (2 - 5);
y = -abs(x) / 2;
print y;
print sin(pi / 2) + cos(0) + tan(0);
```

Cada sentencia debe terminar en `;`.

## Ver tokens, árbol o traza (opcional)

Al inicio de `main.py` hay tres variables. Cambiarlas a `True` para activar cada una:

```python
MOSTRAR_TOKENS = False
MOSTRAR_ARBOL = False
MOSTRAR_TRAZA = False
```

## Tipos de errores

- **Léxico:** carácter no reconocido (por ejemplo `@`).
- **Sintáctico:** la sentencia no cumple la gramática (por ejemplo falta `;`).
- **Semántico:** variable no definida, división o módulo por cero, o argumento fuera de dominio.

## Gramática

```
Programa  → ListaSent
ListaSent → Sent ListaSent | ε
Sent      → id = Expr ; | print Expr ;
Expr      → Term ExprP
ExprP     → + Term ExprP | - Term ExprP | ε
Term      → Factor TermP
TermP     → * Factor TermP | / Factor TermP | % Factor TermP | ε
Factor    → - Factor | Primario
Primario  → num | id | ( Expr ) | Func ( Expr )
Func      → abs | sin | cos | tan
```

## Pruebas

Pendientes.
