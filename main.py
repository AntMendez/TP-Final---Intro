from dataclasses import dataclass
from flask import Flask, redirect, url_for, request, render_template, jsonify
app = Flask(__name__, static_url_path='/templates')
from models import db, Libro, Puntuacion, Comentario

app = Flask(__name__)
port = 5000

app.config['SQLALCHEMY_DATABASE_URI']= 'postgresql+psycopg2://postgres:123456@localhost:5432/tp_final'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False




@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/libros/<id_libro>')
def get_libro_by_id(id_libro):
    try:
        libro = Libro.query.get(id_libro)
        libro_data = {
            'id': libro.id,
            'nombre': libro.nombre,
            'autor': libro.autor,
            'img': libro.img,
            'pdf': libro.pdf,
            'descripcion': libro.descripcion,
            'categoria': libro.categoria
        }
        return jsonify(libro_data)
        
    except Exception as error:
        print('Error', error)
        return jsonify({'message': 'Internal server error'}), 500

@app.route('/libros') 
def get_libros():
    try:
        libros = Libro.query.all()
        libros_data = []
        for libro in libros:
            libro_data = {
                'id': libro.id,
                'nombre': libro.nombre,
                'autor': libro.autor,
                'img': libro.img,
                'pdf': libro.pdf,
                'descripcion': libro.descripcion,
                'categoria': libro.categoria
            }
            libros_data.append(libro_data)
        # return jsonify({'libros': libros_data})
        # print(libros_data) #se imprime en terminal
        midle=" "
        for libro in range(0,len(libros_data)):
            print(libro)
            # for key in libros_data[libro]:
            #     key_value=str(libros_data[libro][key])
            #     print(f'{key}: {key_value}')
            nombre=str(libros_data[libro]['nombre'])
            midle+= f"<p>{nombre}<a href='{libros_data[libro]['pdf']}'><img src='{libros_data[libro]['img']}' width='100'></a></p>"
        return midle

    except Exception as error:
        print('Error', error)
        return jsonify({'message': 'Internal server error'}), 500

@app.route('/publicar', methods=['GET'])
def nuevo_libros():
    return render_template('form.html')

@app.route('/libros', methods=['POST'])
def add_libros():
    try: 
        # data= request.json        
        # nombre= request.form['nombre']
        # autor= request.form['autor']
        # img = request.form['img']
        # pdf = request.form['pdf']
        # descripcion = request.form['descripcion']
        # categoria = request.form['categoria']

        data= request.json        
        nombre= data.get('nombre')
        autor= data.get('autor')
        img = data.get('img')
        pdf = data.get('pdf')
        descripcion = data.get('descripcion')
        categoria = data.get('categoria')

        nuevo_libro= Libro(nombre=nombre, autor=autor, img=img, pdf=pdf, descripcion=descripcion, categoria=categoria)
        # print('ID:  ',str(nuevo_libro.id))
        db.session.add(nuevo_libro)
        db.session.commit()
        return jsonify({'libro': {'id':nuevo_libro.id, 'name':nuevo_libro.nombre,'categoria':nuevo_libro.categoria} }),201

    except Exception as error:
        print('Error', error)
        return jsonify({'message': 'Internal server error'}), 500

# curl -v -X POST 'http://localhost:5000/libros'  '{
#     "nombre": "Diego",
#     "autor": 27,
#     "img": 'img_1',
#     "pdf": 'pdf_1',
#     "descripcion": 'desc_1',
#     "categoria": 'catg_1'
# }'



if __name__ == '__main__':
    db.init_app(app)
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', debug=True, port=port)




