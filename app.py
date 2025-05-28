from flask import Flask, request, jsonify
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

# Configuración de la base de datos
db_config = {
    'host': '186.81.194.142',
    'port': 3306,
    'user': 'root',
    'password': 'Database',
    'database': 'mercadoMasivo'
}

def get_db_connection():
    try:
        connection = mysql.connector.connect(**db_config)
        return connection
    except Error as e:
        print(f"Error al conectar a MySQL: {e}")
        return None

@app.route('/login', methods=['POST'])
def login():
    data = request.form
    cedula = data.get('usuario')
    clave = data.get('clave')
    
    connection = get_db_connection()
    if not connection:
        return jsonify({'status': 'error', 'message': 'Error de conexión a la base de datos'}), 500
    
    try:
        cursor = connection.cursor(dictionary=True)
        query = "SELECT nombre, apellido FROM Usuario WHERE cedula = %s AND clave = %s"
        cursor.execute(query, (cedula, clave))
        user = cursor.fetchone()
        
        if user:
            return jsonify({
                'status': 'ok',
                'nombre': f"{user['nombre']} {user['apellido']}"
            })
        else:
            return jsonify({'status': 'error', 'message': 'Usuario o contraseña incorrectos'}), 401
    except Error as e:
        print(f"Error en la consulta: {e}")
        return jsonify({'status': 'error', 'message': 'Error en el servidor'}), 500
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

@app.route('/')
def index():
    return app.send_static_file('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)