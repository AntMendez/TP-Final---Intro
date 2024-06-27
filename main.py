from dataclasses import dataclass
from flask import Flask, redirect, url_for, request, render_template
app = Flask(__name__, static_url_path='/templates')
from models import db, Libro, Puntuacion, Comentario

app = Flask(__name__)
port = 5000

app.config['SQLALCHEMY_DATABASE_URI']= 'postgresql+psycopg2://postgres:123456@localhost:5432/tp_final'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False




@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/libros')
def get_libros():

    return 




if __name__ == '__main__':
    db.init_app(app)
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', debug=True, port=port)











