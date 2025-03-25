from flask import Flask, render_template, request
from logica.funciones import *

# Creo una instancia de Flask
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', active_page='index')

@app.route('/caso1', methods=["GET", 'POST'])
def caso1():
    error = None  # Inicializamos la variable error
    if request.method == 'POST':
        try:
            # Obtener los datos del formulario
            hora = request.form['horaSalida']
            distancia = float(request.form['distancia'])
            tipoDistancia = request.form['medidaDistancia']

            # Datos Tren 1
            idTren1 = 1
            velocidad1 =  float(request.form['velocidadTren1'])
            tipoVelocidad1 = request.form['medidaVelocidadTren1']
            estacionInicial1 = request.form.get('estacionInicioTren1', None)  # None si no se selecciona
            estacionFinal1 = request.form.get('estacionFinTren1', None)  # None si no se selecciona

            # Datos Tren 2
            idTren2 = 2
            velocidad2 =  float(request.form['velocidadTren2'])
            tipoVelocidad2 = request.form['medidaVelocidadTren2']
            estacionInicial2 = request.form.get('estacionInicioTren2', None)  # None si no se selecciona
            estacionFinal2 = request.form.get('estacionFinTren2', None)  # None si no se selecciona

            # Si hay un error de validación, retornamos al formulario con el error
            if error:
                return render_template('caso1.html', active_page='caso1', error=error)

            # Armar Lista de Trenes
            trenes = [
                {'idTren': idTren1, 'velocidad': velocidad1, 'tipoVelocidad': tipoVelocidad1, 'estacionInicial': estacionInicial1, 'estacionFinal': estacionFinal1},
                {'idTren': idTren2, 'velocidad': velocidad2, 'tipoVelocidad': tipoVelocidad2, 'estacionInicial': estacionInicial2, 'estacionFinal': estacionFinal2},  
            ]
            
            # Convertir la hora de salida
            try:
                hora = hora.split(':')
                hora = [int(hora[0]), int(hora[1])]  # Asumimos que hora_salida está en formato 'HH:MM'
            except ValueError:
                error = 'Formato de hora incorrecto. Asegúrese de ingresar la hora en formato HH:MM.'
                return render_template('caso1.html', active_page='caso1', error=error)

            # Llamar a la función de cálculo
            resultados = calcularCruceEntreTrenes(trenes, distancia, tipoDistancia, hora)

            if isinstance(resultados, tuple):
                tiempoCruce, tiempo, distanciaCruce, distanciaRecorridaTren1, distanciaRecorridaTren2, trenes = resultados
                # Mostrar el resultado o retornar los datos como respuesta
                return render_template('caso1.html', 
                                       active_page='caso1', 
                                       tiempoCruce=tiempoCruce, 
                                       tiempo=tiempo, 
                                       distanciaCruce=distanciaCruce,
                                       distanciaRecorridaTren1=distanciaRecorridaTren1, 
                                       distanciaRecorridaTren2=distanciaRecorridaTren2,
                                       trenes=trenes,
                                       horaIngresada=hora)
            else:
                # Si el cálculo falla, retornamos el mensaje de error
                error = resultados  # Aquí asignamos el mensaje de error a la variable
        except ValueError as e:
            error = str(e)  # Capturamos el error y lo pasamos al template

    return render_template('caso1.html', active_page='caso1', error=error)


@app.route('/caso2', methods=["GET", "POST"])
def caso2():
    error = None
    resultados = None
    
    if request.method == 'POST':
        try:
            # Obtener y validar datos
            altura = float(request.form['altura'])
            tipoAltura = request.form['medidaAltura']
            velocidadInicial = float(request.form['velocidadInicial'])
            tipoVelocidadInicial = request.form['tipoVelocidadInicial']
            
            # Validar valores positivos
            if altura <= 0 or velocidadInicial <= 0:
                raise ValueError("Los valores deben ser mayores que cero")
            
            # Calcular trayectoria
            resultados = calcularTrayectoriaProyectil(
                altura, velocidadInicial, tipoAltura, tipoVelocidadInicial
            )
            
            if isinstance(resultados, str):  # Si es un mensaje de error
                error = resultados
            
        except ValueError as e:
            error = f"Error en los datos ingresados: {str(e)}"
        except Exception as e:
            error = f"Error inesperado: {str(e)}"
    
    return render_template(
        'caso2.html',
        active_page='caso2',
        error=error,
        resultado=resultados if isinstance(resultados, dict) else None
    )
    
if __name__ == "__main__":
    app.run(debug=True, port=1602)
