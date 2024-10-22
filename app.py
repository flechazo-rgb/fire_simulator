from flask import Flask, render_template, request, jsonify, session
import random

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Necesario para usar sesiones

# Definimos los tipos de incendio
incendios = ['forestal', 'edificio', 'cocina', 'gasolinera', 'almacén industrial']

# Puntuaciones correctas por cada tipo de incendio
respuestas_correctas = {
    'forestal': 'agua',  # Por ejemplo, agua para incendios forestales
    'edificio': 'químico',
    'cocina': 'químico',
    'gasolinera': 'polvo',
    'almacén industrial': 'químico'
}

# Ruta principal
@app.route('/')
def index():
    if 'puntos' not in session:
        session['puntos'] = 0

    incendio_actual = random.choice(incendios)
    session['incendio_actual'] = incendio_actual

    return render_template('index.html', incendio=incendio_actual, puntos=session['puntos'])

# Ruta para manejar la selección del usuario
@app.route('/seleccionar', methods=['POST'])
def seleccionar():
    if 'puntos' not in session:
        session['puntos'] = 0

    # Recibimos la selección del usuario
    seleccion = request.form.get('seleccion')
    incendio_actual = session['incendio_actual']

    # Evaluamos si la respuesta es correcta
    if seleccion == respuestas_correctas[incendio_actual]:
        session['puntos'] += 10  # Agrega 10 puntos si es correcto
    else:
        session['puntos'] -= 5  # Penaliza 5 puntos si es incorrecto

    # Verificar si ha alcanzado los 100 puntos
    if session['puntos'] >= 100:
        return jsonify({'status': 'win', 'mensaje': '¡Has alcanzado 100 puntos! ¡Ganaste!'})

    # Actualiza el tipo de incendio y continúa
    nuevo_incendio = random.choice(incendios)
    session['incendio_actual'] = nuevo_incendio

    return jsonify({'status': 'continue', 'nuevo_incendio': nuevo_incendio, 'puntos': session['puntos']})

if __name__ == '__main__':
    app.run(debug=True)
