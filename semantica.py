import math


class ErrorSemantico(Exception):
    pass


def mostrar_valor(valor):
    if valor.is_integer():
        print(int(valor))        
    else:
        print(valor)


class Semantica:
    def __init__(self):
        self.variables = {"pi": math.pi, "e": math.e}

    def ejecutar(self, raiz):
        lista = raiz.hijos[0]
        while len(lista.hijos) > 0:
            sentencia = lista.hijos[0]

            if sentencia.hijos[0].simbolo == "id":
                nombre = sentencia.hijos[0].token.lexema
                valor = self.expr(sentencia.hijos[2])
                self.variables[nombre] = valor
            else:
                valor = self.expr(sentencia.hijos[1])
                mostrar_valor(valor)

            lista = lista.hijos[1]

    def expr(self, nodo):
        valor = self.term(nodo.hijos[0])
        return self.expr_p(nodo.hijos[1], valor)

    def expr_p(self, nodo, acumulado):
        if len(nodo.hijos) == 0:         
            return acumulado
        operador = nodo.hijos[0].simbolo
        derecho = self.term(nodo.hijos[1])
        if operador == "+":
            acumulado = acumulado + derecho
        else:
            acumulado = acumulado - derecho
        return self.expr_p(nodo.hijos[2], acumulado)

    def term(self, nodo):
        valor = self.factor(nodo.hijos[0])
        return self.term_p(nodo.hijos[1], valor)

    def term_p(self, nodo, acumulado):
        if len(nodo.hijos) == 0:          
            return acumulado
        operador = nodo.hijos[0].simbolo
        token_op = nodo.hijos[0].token
        derecho = self.factor(nodo.hijos[1])

        if operador == "*":
            acumulado = acumulado * derecho
        else:
            if derecho == 0:
                if operador == "/":
                    nombre = "división"
                else:
                    nombre = "módulo"
                raise ErrorSemantico("Línea " + str(token_op.linea)
                                     + ", columna " + str(token_op.columna)
                                     + ": " + nombre + " por cero")
            if operador == "/":
                acumulado = acumulado / derecho
            else:
                acumulado = acumulado % derecho
        return self.term_p(nodo.hijos[2], acumulado)

    def factor(self, nodo):
        if nodo.hijos[0].simbolo == "-":
            return -self.factor(nodo.hijos[1])
        return self.primario(nodo.hijos[0])

    def primario(self, nodo):
        primero = nodo.hijos[0]

        if primero.simbolo == "num":
            return float(primero.token.lexema)

        if primero.simbolo == "id":
            token = primero.token
            if token.lexema not in self.variables:
                raise ErrorSemantico("Línea " + str(token.linea)
                                     + ", columna " + str(token.columna)
                                     + ": la variable '" + token.lexema
                                     + "' no ha sido definida")
            return self.variables[token.lexema]

        if primero.simbolo == "(":
            return self.expr(nodo.hijos[1])

        token_func = primero.hijos[0].token
        argumento = self.expr(nodo.hijos[2])
        return self.aplicar_funcion(token_func, argumento)

    def aplicar_funcion(self, token, x):
        try:
            if token.tipo == "abs":
                return abs(x)
            if token.tipo == "sin":
                return math.sin(x)
            if token.tipo == "cos":
                return math.cos(x)
            if token.tipo == "tan":
                return math.tan(x)
        except ValueError:
            raise ErrorSemantico("Línea " + str(token.linea) + ", columna "
                                 + str(token.columna)
                                 + ": argumento fuera de dominio para "
                                 + token.tipo)
