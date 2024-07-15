from dataclasses import dataclass
from flask import Flask, redirect, url_for, request, render_template, jsonify 
app = Flask(__name__, static_url_path='/templates')
from models import db, Libro,  Comentario, Coleccion #,Puntuacion



app = Flask(__name__)
port = 5000

app.config['SQLALCHEMY_DATABASE_URI']= 'postgresql+psycopg2://postgres:123456@localhost:5432/tp_final'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

# curl -X PUT -H "Content-Type":"application/json" -d '{"nombre": "Diego", "autor":"autor_1","img": "img_1","pdf":"pdf_1","descripcion": "desc_1","categoria": "catg_1"}' "http://localhost:5000/catalogo/libros/27" 

@app.route("/colecciones/todas")
def get_colecciones_todas():
    try:
        colecciones = Coleccion.query.all()
        colecciones_data=[]
        colecciones_nombres=set()
        for coleccion in colecciones:
            if not (coleccion.nombre) in colecciones_nombres:
                coleccion_data = {
                    'id':coleccion.id,
                    'nombre':coleccion.nombre
                }
                colecciones_nombres.add(coleccion.nombre)
                colecciones_data.append(coleccion_data)
        return jsonify({'colecciones':colecciones_data}),200
    except Exception as error:
        print('Error', error)
        return jsonify({'message': 'Internal server error'}), 500


@app.route("/colecciones")
def get_colecciones():
    try:
        colecciones = Coleccion.query.all()
        colecciones_data=[]
        colecciones_nombres=set()
        for coleccion in colecciones:
            if not (coleccion.nombre) in colecciones_nombres:
                coleccion_data = {
                    'id':coleccion.id,
                    'nombre':coleccion.nombre
                }
                colecciones_nombres.add(coleccion.nombre)
                colecciones_data.append(coleccion_data)
        #return jsonify({'colecciones':colecciones_data}),200
        return render_template('colecciones.html',data=colecciones_data)
    
    except Exception as error:
        print('Error', error)
        return jsonify({'message': 'Internal server error'}), 500

    

@app.route("/colecciones", methods=['POST'])
def crear_coleccion():
    try:
        data= request.json

        nombre= data.get('nombre')

        id_libro = data.get('id_libro')

        coleccion= Coleccion(id_libro=id_libro,nombre=nombre)
        db.session.add(coleccion)
        db.session.commit()

        return jsonify({'coleccion':coleccion.id}) #render_template con index.html donde aparecerian todas las colecciones incluida la nueva
    except Exception as error:
        print('Error', error)
        return jsonify({'message': 'Internal server error'}), 500

@app.route("/colecciones/<nombre_coleccion>/catalogo")
def get_coleccion_catalogo(nombre_coleccion):
    try:
        query_coleccion= Coleccion.query.filter_by(nombre=nombre_coleccion)
        coleccion_data=[]
        for libro_coleccion in query_coleccion:
            libro=Libro.query.filter_by(id=libro_coleccion.id_libro).first()
            libro_data ={
                'id': libro.id,
                'nombre': libro.nombre,
                'autor': libro.autor,
                'img': libro.img,
                'pdf': libro.pdf,
                'descripcion': libro.descripcion,
                'categoria': libro.categoria
            }
            coleccion_data.append(libro_data)
            
        return jsonify({'coleccion':coleccion_data})
        #return render_template('libros.html',data=coleccion_data)
    except Exception as error:
        print('Error', error)
        return jsonify({'message': 'Internal server error'}), 500
@app.route("/colecciones/<nombre_coleccion>")
def get_coleccion(nombre_coleccion):
    try:
        query_coleccion= Coleccion.query.filter_by(nombre=nombre_coleccion)
        coleccion_data=[]
        for libro_coleccion in query_coleccion:
            libro=Libro.query.filter_by(id=libro_coleccion.id_libro).first()
            libro_data ={
                'id': libro.id,
                'nombre': libro.nombre,
                'autor': libro.autor,
                'img': libro.img,
                'pdf': libro.pdf,
                'descripcion': libro.descripcion,
                'categoria': libro.categoria
            }
            coleccion_data.append(libro_data)
            
        #return jsonify({'coleccion':coleccion_data})
        return render_template('libros.html',data=coleccion_data)
    except Exception as error:
        print('Error', error)
        return jsonify({'message': 'Internal server error'}), 500


@app.route("/colecciones/<nombre_coleccion>", methods=['POST'])
def agregar_libro_a_coleccion(nombre_coleccion):
    try:
        id_libro = request.json.get('id_libro')
        coleccion = Coleccion(id_libro=id_libro,nombre=nombre_coleccion)
        db.session.add(coleccion)
        db.session.commit()
        return jsonify({'coleccion':coleccion.id})
    except Exception as error:
        print('Error', error)
        return jsonify({'message': 'Internal server error'}), 500



@app.route("/colecciones/<nombre_coleccion>", methods=['DELETE'])
def remover_libro_de_coleccion(nombre_coleccion):
    try:
        id_libro = request.json.get('id_libro')
        Coleccion.query.filter_by(id_libro=id_libro,nombre=nombre_coleccion).delete()
        db.session.commit()
        return jsonify({'success':'El libro ' +id_libro+' fue removido exitosamente.'}), 200
    except Exception as error:
        print('Error', error)
        return jsonify({'message': 'Internal server error'}), 500

@app.route("/colecciones", methods=['DELETE'])
def eliminar_coleccion():
    try:
        data= request.json
        nombre=data.get('nombre')
        Coleccion.query.filter_by(nombre=nombre).delete()
        db.session.commit()
        return jsonify({'success':'La coleccion' +nombre+' fue borrada exitosamente.'}),200
    except Exception as error:
        print('Error', error)
        return jsonify({'message': 'Internal server error'}), 500

@app.route("/editar/<id_libro>",methods = ["PUT"])
def editar_libro(id_libro):
    try: 
        data = request.json        
        nombre= data.get('nombre')
        autor= data.get('autor')
        img = data.get('img')
        pdf = data.get('pdf')
        descripcion = data.get('descripcion')
        categoria = data.get('categoria')
        
        
        libro = Libro.query.filter_by(id = id_libro).first()
        libro.nombre=nombre
        libro.autor=autor
        libro.img=img
        libro.pdf=pdf
        libro.descripcion=descripcion
        libro.categoria=categoria
        db.session.commit()
        return jsonify({'libro': {'id':libro.id, 'name':libro.nombre,'categoria':libro.categoria} }),201
    
    except Exception as error:
        print('Error', error)
        return jsonify({'message': 'Internal server error'}), 500
"""@app.route("/editar/<id_libro>", methods = ["POST"])
def get_editar_libro(id_libro):
    try:
        libro_data = {}
        try:
            libro=Libro.query.filter_by_id(id=id_libro).first()
            libro_data ={
                'id': libro.id,
                'nombre': libro.nombre,
                'autor': libro.autor,
                'img': libro.img,
                'pdf': libro.pdf,
                'descripcion': libro.descripcion,
                'categoria': libro.categoria
            }
        except Exception as error:
            print('Error', error)
            return jsonify({'message': 'Internal server error'}), 500
       
        return render_template('actualizar.html',data=libro_data)
    except Exception as error:
        print('Error', error)
        return jsonify({'message': 'Internal server error'}), 500"""    


@app.route("/editar/<id_libro>")
def modificar_libro(id_libro):
    try:
        libro_data = {}
        try:
            libro=Libro.query.filter_by(id=id_libro).first()
            libro_data ={
                'id': libro.id,
                'nombre': libro.nombre,
                'autor': libro.autor,
                'img': libro.img,
                'pdf': libro.pdf,
                'descripcion': libro.descripcion,
                'categoria': libro.categoria
            }
            return render_template('actualizar.html',data=libro_data)
        except Exception as error:
            print('Error', error)
            return jsonify({'message': 'Internal server error'}), 500
    except Exception as error:
        print('Error', error)
        return jsonify({'message': 'Internal server error'}), 500
    

@app.route("/catalogo/<id_libro>", methods = ["DELETE"])
def borrar_libro(id_libro):
    try:
        try:
            print(Comentario.query.filter_by(id_libro=id_libro).delete())
            db.session.commit()
        except Exception as error:
            print('Error', error)
            return jsonify({'message': 'Internal server error'}), 500
        
        print(Libro.query.filter_by(id=id_libro).delete())
        db.session.commit()
        return jsonify({'success':'El libro ' +id_libro+' fue borrado exitosamente'}), 500
    except Exception as error:
        print('Error', error)
        return jsonify({'message': 'Internal server error'}), 500



@app.route('/')
def hello_world():
    try:
        libros_data=[]
        libros=Libro.query.all()
        for libro in libros:
            libro_data ={
                'id': libro.id,
                'nombre': libro.nombre,
                'autor': libro.autor,
                'img': libro.img,
                'pdf': libro.pdf,
                'descripcion': libro.descripcion,
                'categoria': libro.categoria
            }
            libros_data.append(libro_data)
        return render_template('index.html',data=libros_data[::-1])
    except Exception as error:
        print('Error', error)
        return jsonify({'message': 'Internal server error'}), 500

@app.route('/comentarios/<id_libro>')
def get_comentarios_by_id(id_libro):
    try:
        comentarios =[]
        query_comentarios = Comentario.query.filter_by(id_libro=id_libro)
        for comentario in query_comentarios:
            comentario_data = {
                'id': comentario.id,
                'id_libro':comentario.id_libro,
                'comentario': comentario.comentarios
                }
            comentarios.append(comentario_data)
        return jsonify({'comentarios':comentarios})
    except Exception as error:
        print('Error', error)
        return jsonify({'message': 'Internal server error'}), 500

@app.route('/comentarios/<id_libro>',methods=['POST'])
def agregar_comentarios(id_libro):
    try:
        data= request.json   
        print(data)
        
        comentarios=data.get('comentarios')  
        print(comentarios) 

        nuevo_comentario=Comentario(id_libro=id_libro, comentarios=comentarios)
        print(nuevo_comentario)

        db.session.add(nuevo_comentario)
        db.session.commit()
        
        print(nuevo_comentario.comentarios)
        return jsonify({'comentario':nuevo_comentario.comentarios})
    except Exception as error:
        print('Error', error)
        return jsonify({'message': 'Internal server error'}), 500
          
@app.route('/puntuaciones/<id_libro>')
def get_puntuacion_by_id(id_libro):   
    try:
        
        puntuacion = Libro.query.filter_by(id=id_libro).first().puntuacion
       
        if not puntuacion:
            puntuacion ="No tiene puntuacion"
        print(puntuacion)

        return jsonify({'puntuacion':puntuacion})
    except Exception as error:
        print('Error', error)
        return jsonify({'message': 'Internal server error'}), 500


@app.route('/puntuaciones/<id_libro>',methods=['POST'])
def agregar_puntuacion_by_id(id_libro):
    try:
        puntuacion_data = request.json
        puntuacion = puntuacion_data.get('puntuacion')
        libro = Libro.query.filter_by(id=id_libro).first()
        libro.puntuacion=puntuacion
        
        db.session.commit()
        
        return jsonify({'puntuacion':puntuacion}),201
    except Exception as error:
        print('Error', error)
        return jsonify({'message': 'Internal server error'}), 500
    


@app.route('/<categoria>')
def get_libro_by_categoria(categoria):
    try:
        if (categoria not in ['libros','apuntes','examenes']):raise ValueError
        libros=Libro.query.filter_by(categoria=categoria)
        libros_data=[]
        for libro in libros:
            libro_data ={
                'id': libro.id,
                'nombre': libro.nombre,
                'autor': libro.autor,
                'img': libro.img,
                'pdf': libro.pdf,
                'descripcion': libro.descripcion,
                'categoria': libro.categoria
            }
            libros_data.append(libro_data)
        return render_template('libros.html',data=libros_data)
    except Exception as error:
        print('Error', error)
        return jsonify({'message': 'Internal server error: la url "/'+categoria+'" no existe'}), 500
    
@app.route('/catalogo/<id_libro>')
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
        
        return render_template('libro.html',data=libro_data)
    except Exception as error:
        print('Error', error)
        #return jsonify({'message': 'Internal server error'}), 500
        return redirect('/')
    
@app.route('/catalogo/todos')#/libros/<categoria> o /<categoria> ---> categoria = libros 
def get_todos_libros():
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
        return jsonify({'libros':libros_data}),200

    except Exception as error:
        print('Error', error)
        return jsonify({'message': 'Internal server error'}), 500

@app.route('/catalogo')#/libros/<categoria> o /<categoria> ---> categoria = libros 
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
        return render_template('libros.html', data=libros_data)

    except Exception as error:
        print('Error', error)
        return jsonify({'message': 'Internal server error'}), 500

@app.route('/publicar', methods=['GET'])
def nuevo_libros():
    return render_template('form.html')

@app.route('/catalogo', methods=['POST'])
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
        return jsonify({'success':'algo','libro': {'id':nuevo_libro.id, 'name':nuevo_libro.nombre,'categoria':nuevo_libro.categoria} }),201

    except Exception as error:
        print('Error', error)
        return jsonify({'message': 'Internal server error'}), 500

# curl -v -X PUT 'http://localhost:5000/catalogo/libros/5'  '{
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




