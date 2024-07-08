from dataclasses import dataclass
from flask import Flask, redirect, url_for, request, render_template, jsonify
app = Flask(__name__, static_url_path='/templates')
from models import db, Libro, Puntuacion, Comentario



app = Flask(__name__)
port = 5000

app.config['SQLALCHEMY_DATABASE_URI']= 'postgresql+psycopg2://postgres:123456@localhost:5432/tp_final'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

# curl -X PUT -H "Content-Type":"application/json" -d '{"nombre": "Diego", "autor":"autor_1","img": "img_1","pdf":"pdf_1","descripcion": "desc_1","categoria": "catg_1"}' "http://localhost:5000/libros/27" 

@app.route("/libros/<id_libro>",methods = ["PUT"])
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

@app.route('/comentarios/<id_libro>')
def get_comentarios_by_id(id_libro):
    try:
        comentarios =[]
        query_comentarios = Comentario.query.filter_by(id_libro=id_libro)
        print(query_comentarios)
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
        comentario=data.get('comentario')   
        nuevo_comentario=Comentario(id_libro=id_libro, comentario=comentario)
        db.session.add(nuevo_comentario)
        db.session.commit()
        return jsonify({'comentario':nuevo_comentario.comentarios})
    except Exception as error:
        print('Error', error)
        return jsonify({'message': 'Internal server error'}), 500
            
@app.route('/puntaciones/<id_libro>')
def get_puntuaciones_by_id(id_libro):
    try:
        puntuacion_promedio=0
        puntuaciones = Puntuacion.query.filter_by(id_libro=id_libro)
        for puntuacion in puntuaciones:
            puntuacion_promedio+= puntuacion.puntuacion
        puntuacion_promedio = str(puntuacion_promedio/puntuaciones.length)[:3] #un digito con un decimal
        return jsonify({'puntuacion promedio':puntuacion_promedio,'cantidad puntuaciones': puntuaciones.length})
    except Exception as error:
        print('Error', error)
        return jsonify({'message': 'Internal server error'}), 500



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
            'categoria': libro.categoria,
        }

        midle=""
        nombre=str(libro_data['nombre'])
        midle+= f"<p>{nombre}<a href='{libro_data['pdf']}'><img src='{libro_data['img']}' width='100'></a></p>"
        midle+= f"<button onclick='eliminar_libro({libro_data['id']})'>Eliminar</button>"
        comentarios="""<br> <button onclick="get_comentarios(event)">Cargar comentarios</button>
                        <ul id='lista_comentarios'>Lista de comentarios</ul>
            <script>
                function handle_response(data){
                    if (!data){
                        alert('Error')
                        /*window.location.href = `http://127.0.0.1:5000/libros`*/
                    }else{
                        const ul = document.getElementById('lista_comentarios')
                        var comentarios_json = data
                        for (var i = 0; i < data.comentarios.length; i++){
                            console.log(data.comentarios[i].comentario)
                            const texto = data.comentarios[i].comentario
                            console.log(texto)
                            const li = document.createElement('li')
                            li.innerHTML=texto
                            ul.appendChild(li)
                            }
                        }
                    }
                function get_comentarios(event){
                    event.preventDefault()
                    fetch('http://127.0.0.1:5000/comentarios/"""+id_libro+"""')
                    .then((res)=>res.json())
                    .then(handle_response)
                    .catch((error)=> console.log('ERROR',error))

                    
                }
            </script>
                """
        midle+= comentarios
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
        # print(libros_data) #se imprime en terminal
        midle=" "
        for libro in range(0,len(libros_data)):
            # print(libro)
            # for key in libros_data[libro]:
            #     key_value=str(libros_data[libro][key])
            #     print(f'{key}: {key_value}')
            nombre=str(libros_data[libro]['nombre'])
            midle+= f"<p>{nombre}<a href='/libros/{libros_data[libro]['id']}'><img src='{libros_data[libro]['img']}' width='100'></a></p>"
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

# curl -v -X PUT 'http://localhost:5000/libros/5'  '{
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




