from flask import Flask, request, jsonify
from flask_cors import CORS
import math

app = Flask(__name__)
CORS(app)  # Habilitar CORS

# Función para calcular el EOQ
def calcular_eoq(D, A, H):
    """
    Calcula el Lote Económico de Pedido (EOQ).

    Parámetros:
    D (float): Demanda anual.
    A (float): Costo por orden.
    H (float): Costo de mantener una unidad en inventario por año.

    Retorna:
    float: El número óptimo de unidades por orden.
    """
    return math.sqrt((2 * D * A) / H)

# Ruta para calcular el EOQ
@app.route('/calcular-eoq', methods=['POST'])
def calcular_eoq_endpoint():
    try:
        # Obtener los datos del cuerpo de la solicitud (en formato JSON)
        data = request.json
        D = float(data['demanda_anual'])
        A = float(data['costo_orden'])
        H = float(data['costo_mantener'])

        # Validar que los valores sean positivos
        if D <= 0 or A <= 0 or H <= 0:
            return jsonify({"error": "Los valores deben ser mayores que cero."}), 400

        # Calcular el EOQ
        eoq = calcular_eoq(D, A, H)
        return jsonify({"eoq": eoq})
    except KeyError:
        return jsonify({"error": "Faltan parámetros en la solicitud."}), 400
    except ValueError:
        return jsonify({"error": "Los valores deben ser números válidos."}), 400

# Ruta de inicio (opcional)
@app.route('/')
def inicio():
    return "Bienvenido al Microservicio de Gestión de Inventarios"

# Iniciar la aplicación Flask
if __name__ == '__main__':
    app.run(debug=True, port=5001, host='0.0.0.0')  # Cambiar el puerto a 5001 y permitir conexiones externas