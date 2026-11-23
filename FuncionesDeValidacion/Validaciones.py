def numero_dentro_rangoCerrado(numero, valor_minimo, valor_maximo):
    return valor_minimo <= numero <= valor_maximo


def es_texto_valido(texto, solo_letras=False):
    if len(texto) < 2:
        return False
    if solo_letras:
        for caracter in texto:
            if not (caracter.isalpha() or caracter.isspace()):
                return False
    return True


def pedir_texto(texto, mensaje_error, solo_letras=False):
    entrada = input(texto).strip()
    while not es_texto_valido(entrada, solo_letras):
        entrada = input(mensaje_error).strip()
    return entrada


def pedir_cadena_numerica(texto, long_min, long_max, mensaje_error):
    entrada = input(texto).strip()
    while not (entrada.isdigit() and numero_dentro_rangoCerrado(len(entrada), long_min, long_max)):
        entrada = input(mensaje_error).strip()
    return entrada


def pedir_entero(texto, valor_minimo, valor_maximo, mensaje_error):
    entrada = input(texto).strip()
    while not (entrada.isdigit() and numero_dentro_rangoCerrado(int(entrada), valor_minimo, valor_maximo)):
        entrada = input(mensaje_error).strip()
    return int(entrada)


def pedir_decimal(texto, valor_minimo, valor_maximo, mensaje_error):
    entrada = input(texto).replace(",", ".").strip()
    while not (entrada.replace(".", "", 1).isdigit() and numero_dentro_rangoCerrado(float(entrada), valor_minimo, valor_maximo)):
        entrada = input(mensaje_error).replace(",", ".").strip()
    return float(entrada)
