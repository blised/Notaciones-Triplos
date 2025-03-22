from flask import Flask, render_template, request, jsonify
from collections import deque
import re

app = Flask(__name__, static_folder="static", template_folder="templates")

def match_tokens(expresion):
    """
    Lo que hace este metodo es que tokeniza por asi decir la expresión
    infija en partes: num, varia, ope y ().
    Para que pueda funcionar con o sin espacios en blanco

    No funciono lo que queria hacer XD
    """
    
def verificar_sintaxis(expresion):
    """ Verifica que la sintaxis de la expresión sea correcta """
    pila = []
    operadores = {'+', '-', '*', '/', '^', '%', '='}
    signos_agrupacion = {'(': ')', '{': '}', '[': ']'}
    apertura = signos_agrupacion.keys()
    cierre = signos_agrupacion.values()

    # Verificar caracteres inválidos antes de tokenizar
    sin_espacios = expresion.replace(" ", "")
    if not re.fullmatch(r'[a-zA-Z0-9+\-*/%^=(){}\[\]]*', sin_espacios):
        for c in sin_espacios:
            if not re.fullmatch(r'[a-zA-Z0-9+\-*/%^=(){}\[\]]', c):
                return False, f"Error: carácter no válido detectado ('{c}')."

    # Despues de asegurarnos que no hay caracteres inválidos hacemos lo siguientek
    # Expresión regular que acepta variables alfabéticas
    tokens = re.findall(r'[a-zA-Z]+|\d+|[-+*/%^=(){}\[\]]', expresion)

    for i, token in enumerate(tokens):
        if token in apertura:
            pila.append(token)
        elif token in cierre:
            if not pila:
                return False, "Error de paréntesis: falta un paréntesis de apertura."
            ultimo_abierto = pila.pop()
            if signos_agrupacion[ultimo_abierto] != token:
                return False, f"Error de paréntesis: {ultimo_abierto} no coincide con {token}."
        elif token in operadores:
            # No permitir operadores en el inicio o al final
            if i == 0 or i == len(tokens) - 1:
                return False, "Error de operadores: operador en una posición incorrecta."
            # No permitir operadores consecutivos
            if tokens[i - 1] in operadores or tokens[i + 1] in operadores:
                return False, "Error de operadores: operadores consecutivos no permitidos."
    
    if pila:
        return False, "Error de paréntesis: falta un paréntesis de cierre."
    
    return True, "Expresión válida."

def infija_a_postfija(expresion):
    # Convertir una expresión infia a postfija
    salida = []
    pila = deque()
    precedencia = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3, '%': 3, 
                   '=': 0, '(': 0, '{': 0, '[': 0, ')': 0, '}': 0, ']': 0}
    pares_parentesis = {')': '(', '}': '{', ']': '['}  # Mapear cierre a apertura
    tokens = re.findall(r'[a-zA-Z]+|\d+|[-+*/%^=(){}\[\]]', expresion)
    
    for token in tokens:
        # if token.isnumeric(): al querer evaluar letras y numeros marcar error
        if re.fullmatch(r'[a-zA-Z]+|\d+', token):
            salida.append(token)
        elif token in "({[":
            pila.append(token)
        elif token in ")}]":
            while pila and pila[-1] not in "({[":
                salida.append(pila.pop())
            if pila and pila[-1] == pares_parentesis[token]:  
                pila.pop()
            else:
                return "Error: paréntesis desbalanceados"
        else:
            while pila and precedencia[pila[-1]] >= precedencia[token]:
                salida.append(pila.pop())
            pila.append(token)
    
    while pila:
        salida.append(pila.pop())
    
    return ' '.join(salida)

def infija_a_prefija(expresion):
    """ Convierte una expresión infija a prefija invirtiendo la lógica de infija-postfija """
    expresion = expresion[::-1]  # Invertir la expresión
    expresion = expresion.replace('(', 'temp').replace(')', '(').replace('temp', ')') \
                         .replace('{', 'temp2').replace('}', '{').replace('temp2', '}') \
                         .replace('[', 'temp3').replace(']', '[').replace('temp3', ']')
    postfija = infija_a_postfija(expresion)  # Convertir a postfija
    return ' '.join(postfija.split()[::-1])  # Invertir la postfija para obtener prefija

def resolver_postfija(expresion):
    """ Evalúa una expresión en notación postfija utilizando una pila """
    stack = []
    tokens = expresion.split()
    
    for token in tokens:
        if token.isdigit():
            stack.append(int(token))
        else:
            b = stack.pop()
            a = stack.pop()
            if token == '+':
                stack.append(a + b)
            elif token == '-':
                stack.append(a - b)
            elif token == '*':
                stack.append(a * b)
            elif token == '/':
                stack.append(a / b)
            elif token == '^':
                stack.append(a ** b)
            elif token == '%':
                stack.append(a ** (1/b))
    
    return stack.pop()

# def resolver_postfija_con_triplos(expresion):
#     stack = []
#     triplos = []
#     temp_count = 1
    
#     tokens = expresion.split()
    
#     for token in tokens:
#         if token.isdigit():
#             stack.append(token)
#         else:
#             b = stack.pop()
#             a = stack.pop()
#             temp_var = f"T{temp_count}"  # Generamos una variable temporal
#             triplos.append((token, a, b, temp_var))  # Agregamos el tríplo
#             stack.append(temp_var)  # Usamos la variable temporal para futuros cálculos
#             temp_count += 1
    
#     resultado_final = stack.pop()
#     return resultado_final, triplos  # Devolvemos el resultado y la tabla de tríplos

def generar_triplos(postfija):
    """Generar triplos apartir de una exp postfija"""
    stack = []
    triplos = []
    temp_count = 0
    tokens = postfija.split()

    for token in tokens:
        if token not in {'+', '-', '*', '/', '^', '%', '='}:
            stack.append(token)
        else:
            if token == '=':
                valor = stack.pop()
                variable = stack.pop()
                triplos.append((len(triplos), token, variable, valor, ''))
            else:
                b = stack.pop()
                a = stack.pop()
                temp = f"T{temp_count}"
                triplos.append((len(triplos), token, a, b, temp))
                stack.append(temp)
                temp_count += 1
    return triplos

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/procesar', methods=['POST'])
def procesar():
    try:
        datos = request.json
        expresion_infija = datos.get("expresion", "")

        # Verificar sintaxis
        es_valida, mensaje = verificar_sintaxis(expresion_infija)
        if not es_valida:
            return jsonify({"error": mensaje})

        # Convertir expresiones
        expresion_postfija = infija_a_postfija(expresion_infija)
        expresion_prefija = infija_a_prefija(expresion_infija)

        # Si hay variables alfabéticas, no se puede resolver
        if any(re.match(r'[a-zA-Z]', token) for token in expresion_postfija.split()):
            resultado = "No se puede resolver con variables literales"
        else:
            resultado = resolver_postfija(expresion_postfija)

        triplos = generar_triplos(expresion_postfija)
        print(triplos)

        return jsonify({
            "postfija": expresion_postfija,
            "prefija": expresion_prefija,
            "resultado": resultado,
            "triplos": triplos
        })

    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)