# Intérprete LL(1) en Python

Proyecto de teoría de lenguajes y compiladores que implementa un intérprete basado en análisis predictivo no recursivo utilizando una **gramática LL(1)** para un lenguaje formal de asignaciones y expresiones aritmético-trigonométricas. 

El sistema cubre de extremo a extremo las fases de análisis léxico, análisis sintáctico por tabla con pila, y análisis semántico con tabla de símbolos y ejecución en tiempo de ejecución.

---

## 1. Características y Capacidades

- **Operadores aritméticos binarios:** Suma (`+`), resta (`-`), multiplicación (`*`), división (`/`) y residuo/módulo (`%`).
- **Operador unario:** Negación unaria (`-Factor`).
- **Funciones matemáticas y trigonométricas:** `abs(Expr)`, `sin(Expr)`, `cos(Expr)` y `tan(Expr)` (cálculo de funciones trigonométricas en radianes).
- **Asignación y variables:** Asignación dinámica de variables a memoria con sintaxis `id = Expr;`.
- **Salida estándar:** Instrucción `print Expr;` para evaluar y proyectar resultados en pantalla.
- **Constantes predefinidas:** `pi` ($\pi \approx 3.14159265$) y `e` ($e \approx 2.71828182$) precargadas en el entorno semántico.
- **Sintaxis de comentarios:** Soporte de comentarios de una sola línea mediante el delimitador `#`.
- **Diagnóstico formal de la gramática:** Cálculo e impresión automática de conjuntos $\text{PRIMEROS}$, $\text{SIGUIENTES}$, $\text{PREDICCIÓN}$ y la matriz de análisis $M[A, a]$ (tabla LL(1)), verificando la ausencia de conflictos.

---

## 2. Estructura del Repositorio

```text
Tarea_Gramatica_LL1/
│
├── lex.py                # Analizador léxico: tokenizador, manejo de posiciones y ErrorLexico
├── gramatica.py          # Definición de producciones, cálculo de PRIMEROS/SIGUIENTES y tabla LL(1)
├── parser_ll1.py         # Analizador sintáctico predictivo con pila y generación del AST
├── semantica.py          # Analizador semántico: tabla de símbolos, control de tipos y evaluación
├── main.py               # Menú principal interactivo y ejecución por archivo
├── README.md             # Documentación técnica del proyecto
│
└── pruebas/              # Batería de pruebas organizadas por escenarios (.txt)
    ├── prueba1_aritmetica.txt
    ├── prueba2_funciones.txt
    ├── prueba3_error_lexico.txt
    ├── prueba4_error_sintactico.txt
    ├── prueba5_error_variable.txt
    └── prueba6_error_division_cero.txt
```


---

## 3. Especificación Formal de la Gramática

La gramática libre de contexto se encuentra factorizada por la izquierda y no posee recursión izquierda, garantizando la propiedad LL(1):

```text
(1)  Programa  → ListaSent
(2)  ListaSent → Sent ListaSent
(3)  ListaSent → ε
(4)  Sent      → id = Expr ;
(5)  Sent      → print Expr ;
(6)  Expr      → Term ExprP
(7)  ExprP     → + Term ExprP
(8)  ExprP     → - Term ExprP
(9)  ExprP     → ε
(10) Term      → Factor TermP
(11) TermP     → * Factor TermP
(12) TermP     → / Factor TermP
(13) TermP     → % Factor TermP
(14) TermP     → ε
(15) Factor    → - Factor
(16) Factor    → Primario
(17) Primario  → num
(18) Primario  → id
(19) Primario  → ( Expr )
(20) Primario  → Func ( Expr )
(21) Func      → abs
(22) Func      → sin
(23) Func      → cos
(24) Func      → tan
```

---

## 4. Requisitos y Ejecución

- **Requisitos del sistema:** Python 3.6 o superior (librería estándar, sin dependencias externas).
- **Ejecución del intérprete:**
  ```bash
  python3 main.py
  ```
  *(o `python main.py` en entornos Windows).*

### Menú de Opciones

```text
===== INTÉRPRETE LL(1) =====
1. Mostrar gramática, PRIMEROS, SIGUIENTES, PREDICCIÓN y tabla
2. Modo interactivo
3. Ejecutar un archivo
0. Salir
```

- **Opción 1:** Imprime el listado de reglas gramaticales, los conjuntos directores de cada no terminal y la matriz predictiva calculada.
- **Opción 2:** Habilita el shell interactivo (`>>>`) para evaluar sentencias terminadas en `;`. Escribir `salir` para retornar al menú.
- **Opción 3:** Solicita la ruta de un script de prueba para procesarlo completamente (ej. `pruebas/prueba1_aritmetica.txt`).
- **Opción 0:** Finaliza el programa.

---

## 5. Batería de Pruebas (`pruebas/`)

Para ejecutar los archivos de prueba creados, selecciona la **opción 3** en la consola principal e introduce la ruta correspondiente con el prefijo de la carpeta `pruebas/`:

### Prueba 1: `pruebas/prueba1_aritmetica.txt`
Valida la jerarquía de operadores ($*, /, \% > +, -$), paréntesis asociativos, signo unario e impresión de variables.
```text
a = 10;
b = 4;
res1 = a + b * 2;
res2 = (a + b) * 2;
res3 = 17 % 5;
res4 = -res1 + 5;

print res1;
print res2;
print res3;
print res4;
```
**Salida esperada:**
```text
18
28
2
-13
```

---

### Prueba 2: `pruebas/prueba2_funciones.txt`
Evalúa números con parte decimal, las constantes predefinidas `pi` y `e`, y las funciones trigonométricas y matemáticas.
```text
angulo = pi / 2;
s = sin(angulo);
c = cos(0);
t = tan(0);
val_abs = abs(-25.4);
euler = e;

print s;
print c + t;
print val_abs;
print euler;
```
**Salida esperada:**
```text
1
1
25.4
2.718281828459045
```

---

### Prueba 3: `pruebas/prueba3_error_lexico.txt`
Verifica la detección y contención de errores léxicos ante caracteres no contemplados en el alfabeto del lenguaje (ejemplo: `@`).
```text
radio = 5;
area = pi * radio @ 2;
print area;
```
**Salida esperada:**
```text
[Error léxico] Línea 3, columna 16: carácter no reconocido '@'
```

---

### Prueba 4: `pruebas/prueba4_error_sintactico.txt`
Evalúa el rechazo sintáctico por parte de la tabla predictiva LL(1) al omitir el delimitador terminal `;`.
```text
x = 15 + 3
y = 10;
print x + y;
```
**Salida esperada:**
```text
[Error sintáctico] Línea 2, columna 1: se encontró 'y'; se esperaba: %, ), *, +, -, /, ;
```

---

### Prueba 5: `pruebas/prueba5_error_variable.txt`
Verifica el análisis semántico cuando se intenta evaluar un identificador que no existe en la tabla de símbolos.
```text
base = 20;
altura = 10;
area = (base * altura_triangulo) / 2;
print area;
```
**Salida esperada:**
```text
[Error semántico] Línea 4, columna 16: la variable 'altura_triangulo' no ha sido definida
```

---

### Prueba 6: `pruebas/prueba6_error_division_cero.txt`
Verifica la protección semántica en operaciones de división o cálculo de residuo cuando el divisor resulta en cero.
```text
dividendo = 50;
divisor = 10 - (5 * 2);
print dividendo / divisor;
```
**Salida esperada:**
```text
[Error semántico] Línea 4, columna 17: división por cero
```

---

## 6. Depuración y Trazabilidad

En `main.py` es posible activar flags booleanas para inspeccionar el flujo interno del compilador:

```python
MOSTRAR_TOKENS = True   # Imprime la lista secuencial de tokens detectados
MOSTRAR_ARBOL  = True   # Despliega en consola el árbol de derivación sintáctico (AST)
MOSTRAR_TRAZA  = True   # Muestra la traza paso a paso: PILA, ENTRADA y REGLA aplicada
```
