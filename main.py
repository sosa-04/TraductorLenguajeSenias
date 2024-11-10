from flask import Flask, render_template, Response
from openCamera import gen_frame

app= Flask(__name__)

# Esta es la ruta principal
@app.route('/')
def index():
    return render_template('index.html')

# Ruta para mostrar el video en tiempo real
@app.route('/video')
def video():
    return Response(gen_frame(), mimetype='multipart/x-mixed-replace; boundary=frame')

# Ejecutando la web
if __name__:
    app.run(debug=True)