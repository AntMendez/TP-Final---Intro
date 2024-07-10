from dataclasses import dataclass
from flask import Flask, redirect, url_for, request, render_template, jsonify
app = Flask(__name__, static_url_path='/templates')
from models import db, Libro, Puntuacion, Comentario
from sqlalchemy import update


app = Flask(__name__)
port = 5000

app.config['SQLALCHEMY_DATABASE_URI']= 'postgresql+psycopg2://postgres:123456@localhost:5432/tp_final'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

# curl -X PUT -H "Content-Type":"application/json" -d '{"nombre": "Diego", "autor":"autor_1","img": "img_1","pdf":"pdf_1","descripcion": "desc_1","categoria": "catg_1"}' "http://localhost:5000/libros/27" 

@app.route("/libros/<id_libro>",methods = ["POST"])
def editar_libro(id_libro):
    try: 
        data = request.json        
        nombre= data.get('nombre')
        autor= data.get('autor')
        img = data.get('img')
        pdf = data.get('pdf')
        descripcion = data.get('descripcion')
        categoria = data.get('categoria')
        print('sin modificar '+nombre)

        libro = Libro.query.filter_by(id=id_libro)
        libro.nombre=nombre
        print('Modificado '+nombre)
        libro.autor=autor
        libro.img= img
        libro.pdf=pdf
        libro.descripcion=descripcion
        libro.categoria= categoria
        update(Libro).values({"nombre":nombre,"autor":autor,"img":img,"pdf":pdf,"descripcion": descripcion,"categoria":categoria}).where(Libro.c.id==id_libro)
        db.session.commit()

        return jsonify({'libro': {'id':id_libro, 'name':libro.nombre,'categoria':libro.categoria} }),201

    except Exception as error:
        print('Error', error)
        return jsonify({'message': 'Internal server error'}), 500


@app.route("/libros/<id_libro>", methods = ["DELETE"])
def borrar_libro(id_libro):
    try:
        Libro.query.filter_by(id=id_libro).delete()
        db.session.commit()
        return jsonify({'success':'El libro ' +id_libro+' fue borrado exitosamente'}), 500
    except Exception as error:
        print('Error', error)
        return jsonify({'message': 'Internal server error'}), 500



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

        midle=""
        nombre=str(libro_data['nombre'])
        midle+= f"<p>{nombre}<a href='{libro_data['pdf']}'><img src='{libro_data['img']}' width='100'></a></p>"
        midle+= f"<button onclick='eliminar_libro({libro_data['id']})'>Eliminar</button>"

        # return jsonify(libro_data)
        return midle
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
       
        # midle=" "
        # for libro in range(0,len(libros_data)):

        #     nombre=str(libros_data[libro]['nombre'])
        #     midle+= f"<p>{nombre}<a href='/libros/{libros_data[libro]['id']}'><img src='{libros_data[libro]['img']}' width='100'></a></p>"
        # return midle
        return render_template('libros.html', data = libros_data)
     

    except Exception as error:
        print('Error', error)
        return jsonify({'message': 'Internal server error'}), 500

@app.route('/publicar', methods=['GET'])
def nuevo_libros():
    return render_template('form.html')

@app.route('/libros', methods=['POST'])
def add_libros():
    try: 
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

# curl -v -X PUT 'http://localhost:5000/libros/27'  '{
#     "nombre": "Diego",
#     "autor": 27,
#     "img": 'img_1',
    # "pdf": 'pdf_1',
    # "descripcion": 'desc_1',
    # "categoria": 'catg_1'
# }'



if __name__ == '__main__':
    db.init_app(app)
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', debug=True, port=port)




