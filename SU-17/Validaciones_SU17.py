def numero_dentro_rangoCerrado (numero, valor_minimo, valor_maximo):
    return (valor_minimo <= numero <= valor_maximo)

def pedir_entero (texto, valor_minimo, valor_maximo, mensaje_error):
    entrada = input(texto)
    while (not (entrada.isdigit() and numero_dentro_rangoCerrado(
        int(entrada), valor_minimo,
        valor_maximo))):
        entrada = input(mensaje_error)
    return int(entrada)

def pedir_decimal (texto, valor_minimo, valor_maximo, mensaje_error):
    entrada = input(texto).replace(",", ".").strip()
    while (not (entrada.replace(".", "", 1).isdigit() and numero_dentro_rangoCerrado(float(entrada), valor_minimo, valor_maximo))):
        entrada = input(mensaje_error).replace(",", ".").strip()
    return float(entrada)
