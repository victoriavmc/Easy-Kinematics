import math

#VERIFICAR HORA Y MINUTO INGRESADO
def verificarHoraMinuto(hora, minuto):
    if hora < 0 or hora > 23 or minuto < 0 or minuto > 59:
        return False
    return True

#VERIFICAR SI LOS NUMEROS INGRESADOS SON POSITIVOS
def verificarNumerosPositivos(numero):
    numero=int(numero)
    if numero < 0:
        return False
    return True

#CONVERSORES CASO 1
# Conversor de metros a kilómetros
def conversorMKm(distancia):
    return distancia / 1000

# Conversor de m/s a km/h
def conversorMsAKmH(velocidad):
    return velocidad * 3600 / 1000

# Redondear la distancia también a dos decimales
def redondearDistancia(distancia):
    return round(distancia, 2)

# CONVERSOR CASO 2
# Convierte km/h a m/s
def conversorKmHAms(valor):
    return valor / 3.6

# Convierte kilómetros a metros
def conversorKmM(valor):
    return valor * 1000 

## VERIFICACION SI LAS ESTACIONES SON OPUERTAS 
def verificarEstacionesOpuestas(trenes):
    estaciones = set()
    
    for tren in trenes:
        if not isinstance(tren.get('estacionInicial'), str) or not isinstance(tren.get('estacionFinal'), str):
            raise ValueError(f"El tren {tren.get('idTren', 'desconocido')} tiene estaciones inválidas.")
        
        if tren['estacionInicial'] == tren['estacionFinal']:
            raise ValueError(f"El tren {tren.get('idTren', 'desconocido')} tiene la misma estación de inicio y fin: {tren['estacionInicial']}.")

        estaciones.add((tren['estacionInicial'], tren['estacionFinal']))

    for a, b in estaciones:
        if (b, a) in estaciones:
            return True
    
    return False

# CALCULOS
# CALCULAR TIEMPO HASTA EL CRUCE
def calcularTiempoCruce(tren1, tren2, distancia):
    velocidad1 = tren1['velocidad']
    velocidad2 = tren2['velocidad']

    tiempoCruce = distancia / (velocidad1 + velocidad2)
    
    return tiempoCruce

# CALCULAR A QUE HORA FUE EL CRUCE
def calcularHoraCruce(horaInicial, minutosInicial, tiempoCruce):
    # Convertir tiempo de cruce a segundos
    tiempoCruceSegundos = tiempoCruce * 3600

    # Convertir hora y minutos iniciales a segundos
    segundosIniciales = horaInicial * 3600 + minutosInicial * 60
    # Calcular el tiempo total en segundos
    tiempoTotalSegundos = tiempoCruceSegundos + segundosIniciales

    # Calcular días, horas, minutos y segundos
    dias = tiempoTotalSegundos // (24 * 3600)
    tiempoTotalSegundos %= (24 * 3600)
    horas = tiempoTotalSegundos // 3600
    tiempoTotalSegundos %= 3600
    minutos = tiempoTotalSegundos // 60
    segundos = tiempoTotalSegundos % 60

    # Formatear el resultado
    if dias > 0:
        return f"{int(dias)} día(s), {int(horas):02}:{int(minutos):02}:{int(segundos):02}"
    else:
        return f"{int(horas):02}:{int(minutos):02}:{int(segundos):02}"

# CALCULAR DISTANCIA CRUCE
def calcularDistanciaCruce(tren1, tren2, tiempoCruce):
    velocidad1 = tren1['velocidad']
    velocidad2 = tren2['velocidad']

    distanciaCruce = velocidad1 * tiempoCruce
    return distanciaCruce

# CALCULAR DISTANCIA RECORRIDA POR CADA TREN
def calcularDistanciaRecorrida(tren, tiempoCruce):
    velocidad = tren['velocidad']

    distanciaRecorrida = velocidad * tiempoCruce
    return distanciaRecorrida

# UNFICACION DE LOS CALCULOS 

# Caso 1 - Trenes
def calcularCruceEntreTrenes(trenes, distancia, tipoDistancia, hora):
    distanciaFuncion = verificarNumerosPositivos(distancia)
    if not distanciaFuncion:
        return print("La distancia ingresada no es valida.")
    else:
        # Ya convertimos la distancia a km si hace falta
        if tipoDistancia =='m':
            distancia = conversorMKm(distancia)
            #Guardo los cambios en la distancia y el tipo
            distancia = distancia
            tipoDistancia = 'km'
        else:
            pass
    
    horaFuncion = verificarHoraMinuto(hora[0], hora[1])
    if not horaFuncion:
        return ("La hora ingresada no es valida.")
    else:
        pass
    
    #Verifico si la velocidad de cada tren es valida
    for tren in trenes:
        velocidad = tren['velocidad']

        velocidadFuncion = verificarNumerosPositivos(velocidad)
        if not velocidadFuncion:
            return print(f"La velocidad del tren {tren['idTren']} ingresada no es valida.")
        else:
            # Convertir las velocidades a km/h si es necesario
            if tren['tipoVelocidad'] == 'm/s':
                velocidad = conversorMsAKmH(velocidad) 
                #Guardo los cambios en la velocidad y el tipo
                tren['velocidad'] = velocidad
                tren['tipoVelocidad'] = 'km/h'
            else:
                pass
        
    # Verifico si las estaciones son opuestas (A -> B y B -> A)
    if not verificarEstacionesOpuestas(trenes):
        return "No se encontraron trenes con estaciones opuestas. No se puede realizar el cálculo."
    else:
        # Calculo el tiempo de cruce entre los trenes
        tiempoCruce = calcularTiempoCruce(trenes[0], trenes[1], distancia)
        
        # Calcular Hora del Cruce
        tiempo = calcularHoraCruce(hora[0], hora[1], tiempoCruce)
        
        # Calcular distancia de cruce
        distanciaCruce = calcularDistanciaCruce(trenes[0], trenes[1], tiempoCruce)
        
        # Calcular distancia recorrida por cada tren
        distanciaRecorridaTren1 = calcularDistanciaRecorrida(trenes[0], tiempoCruce)
        distanciaRecorridaTren2 = calcularDistanciaRecorrida(trenes[1], tiempoCruce)
        
        return tiempoCruce, tiempo, distanciaCruce, distanciaRecorridaTren1, distanciaRecorridaTren2, trenes
 
 
# Caso 2 - Trayectoria Proyectil Horizontal o tambien llamado Tiro Parabólico Horizontal
def calcularTrayectoriaProyectil(altura, velocidadInicial, tipoAltura, tipoVelocidadInicial):
    alturaFuncion = verificarNumerosPositivos(altura)
    if not alturaFuncion:
        return print("La altura ingresada no es valida.")
    else:
        # Ya convertimos la altura a km si hace falta
        if tipoAltura =='km':
            altura = conversorKmM(altura)
            tipoAltura = 'm'
        else:
            pass

    velocidadInicialFuncion = verificarNumerosPositivos(velocidadInicial)
    if not velocidadInicialFuncion:
        return print("La velocidad ingresada no es valida.")
    else:
        if tipoVelocidadInicial == 'km/h':
            velocidadInicial = conversorMsAKmH(velocidadInicial)
            tipoVelocidadInicial = 'm/s'
        else:
            pass
    
    gravedad = 9.81  # Se mantiene constante, es en m/s² (REDONDEADO)

    # Calcular el tiempo de caída
    tiempoCaida = math.sqrt((2 * altura) / gravedad)

    # Calcular la distancia horizontal
    distanciaHorizontal = velocidadInicial * tiempoCaida
    
    # Velocidad para llegar al suelo
    velocidadCaida= (gravedad) * tiempoCaida
    
    #Velocidad Total
    velocidadTotal = math.sqrt(velocidadInicial**2 + velocidadCaida**2)
    
    #Para saber el angulo cae
    angulo = math.atan2(velocidadCaida, velocidadInicial)
    anguloE2 = math.degrees(angulo)
    
    return {
        "tiempoCaida": round(tiempoCaida, 2),
        "distanciaHorizontal": round(distanciaHorizontal, 2),
        "altura": round(altura, 2),
        "velocidadInicial": round(velocidadInicial, 2),
        "velocidadCaida": round(velocidadCaida,2),
        "velocidadTotal": round(velocidadTotal,2),
        'angulo': round(angulo,2),
        'anguloE2':round(anguloE2,2),
    }