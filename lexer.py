
class Token:
    def __init__(self, tipo, lexema, linea, columna):
        self.tipo = tipo        # 'num', 'id', 'sin', '+', '(', '$', ...
        self.lexema = lexema
        self.linea = linea
        self.columna = columna

    def __str__(self):
        return ("<" + self.tipo + ", " + self.lexema + "> ("
                + str(self.linea) + ":" + str(self.columna) + ")")


class ErrorLexico(Exception):
    pass


PALABRAS_RESERVADAS = ["abs", "sin", "cos", "tan", "print"]
SIMBOLOS = ["+", "-", "*", "/", "%", "(", ")", "=", ";"]


def tokenizar(texto):
    tokens = []
    i = 0
    linea = 1
    columna = 1
    n = len(texto)

    while i < n:
        c = texto[i]

        if c == "\n":
            linea = linea + 1
            columna = 1
            i = i + 1

        elif c == " " or c == "\t" or c == "\r":
            i = i + 1
            columna = columna + 1

        elif c == "#":
            while i < n and texto[i] != "\n":
                i = i + 1
                columna = columna + 1

        elif c.isdigit():
            inicio = i
            col_inicio = columna
            while i < n and texto[i].isdigit():
                i = i + 1
                columna = columna + 1
        
            if i + 1 < n and texto[i] == "." and texto[i + 1].isdigit():
                i = i + 1
                columna = columna + 1
                while i < n and texto[i].isdigit():
                    i = i + 1
                    columna = columna + 1
            lexema = texto[inicio:i]
            tokens.append(Token("num", lexema, linea, col_inicio))

        elif c.isalpha() or c == "_":
            inicio = i
            col_inicio = columna
            while i < n and (texto[i].isalnum() or texto[i] == "_"):
                i = i + 1
                columna = columna + 1
            lexema = texto[inicio:i]
            minuscula = lexema.lower()      
            if minuscula in PALABRAS_RESERVADAS:
                tokens.append(Token(minuscula, lexema, linea, col_inicio))
            else:
                tokens.append(Token("id", lexema, linea, col_inicio))

       
        elif c in SIMBOLOS:
            tokens.append(Token(c, c, linea, columna))
            i = i + 1
            columna = columna + 1

        
        else:
            raise ErrorLexico("Línea " + str(linea) + ", columna "
                              + str(columna) + ": carácter no reconocido '"
                              + c + "'")


    tokens.append(Token("$", "$", linea, columna))
    return tokens
