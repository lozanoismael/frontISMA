from flask import Flask, render_template, redirect, url_for, request
import requests 

app = Flask(__name__)

@app.route('/')
def index():
    # Hacer la petición GET a tu API
    response = requests.get('http://api:8000/imagenes/')
    
    # Verificar si la respuesta es exitosa
    if response.status_code == 200:
        productos = response.json()  # Convertir la respuesta a JSON
    else:
        productos = []  # Si la API falla, enviar una lista vacía
    
    return render_template('index.html', productos=productos)

@app.route('/imagen/delete', methods=['POST'])
def eliminar_producto():
    id_producto = request.form.get('id_producto')
    
    if id_producto:
        url = f'http://api:8000/imagen/delete/{id_producto}'
        response = requests.delete(url)
        
        if response.status_code == 200:
            return redirect(url_for('index'))
        else:
            return "Error al eliminar el producto", response.status_code
    else:
        return "ID de producto no proporcionado", 400

@app.route('/upload', methods=['POST'])
def upload_imagen():
    nombre_producto = request.form.get('nombre_producto')
    if 'imagen' not in request.files or not nombre_producto:
        return "No se ha proporcionado un archivo o el nombre del producto", 400

    file = request.files['imagen']
    
    if file.filename == '':
        return "No se ha seleccionado ninguna imagen", 400

    files = {'file': (file.filename, file.stream, file.content_type)}  # Archivo en formato multipart

    url = f'http://api:8000/upload/?nombre_producto={nombre_producto}'

    response = requests.post(url, files=files)

    if response.status_code == 200:
        return redirect(url_for('index'))
    else:
        return f"Error al subir la imagen: {response.status_code} - {response.text}", response.status_code
    

@app.route('/editar/<int:id_producto>', methods=['GET'])
def mostrar_formulario_editar(id_producto):
    response = requests.get(f'http://api:8000/imagen/{id_producto}')
    
    if response.status_code == 200:
        producto = response.json()
    else:
        return f"Error al obtener el producto: {response.status_code}", response.status_code
    
    return render_template('editar_producto.html', producto=producto)

@app.route('/editar/<int:id_producto>', methods=['POST'])
def guardar_cambios_producto(id_producto):
    nombre_producto = request.form.get('nombre_producto')
    
    file = request.files.get('imagen')
    files = None
    if file and file.filename != '':
        files = {'file': (file.filename, file.stream, file.content_type)}
    
    url = f'http://api:8000/productos/{id_producto}/editar'
    data = {'nombre_producto': nombre_producto}

    if files:
        response = requests.put(url, files=files, data=data)
    else:
        response = requests.put(url, data=data)

    if response.status_code == 200:
        return redirect(url_for('index'))
    else:
        return f"Error al modificar el producto: {response.status_code} - {response.text}", response.status_code




if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
