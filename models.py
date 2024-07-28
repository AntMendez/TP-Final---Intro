import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Libro(db.Model):
	__tablename__ = 'libros'
	id = db.Column(db.Integer, primary_key=True)
	nombre = db.Column(db.String(255), nullable=False)
	autor = db.Column(db.String(255), nullable=False)
	img = db.Column(db.String(255), nullable=False)
	pdf = db.Column(db.String(255), nullable=False)
	descripcion = db.Column(db.String(511), nullable=False)
	categoria = db.Column(db.String(255), nullable=False)
	puntuacion = db.Column(db.Integer,nullable=True)
	favorito= db.Column(db.Boolean,nullable=True)
	vistas = db.Column(db.Integer,default=0,nullable=False)

""" class Puntuacion(db.Model):
	__tablename__ = 'puntuaciones'
	id = db.Column(db.Integer, primary_key=True)
	id_libro = db.Column(db.Integer, db.ForeignKey('libros.id'))
	puntuacion = db.Column(db.Integer, nullable=False)"""

class Comentario(db.Model):
	__tablename__ = 'comentarios'
	id = db.Column(db.Integer, primary_key=True)
	id_libro = db.Column(db.Integer, db.ForeignKey('libros.id'))
	comentarios = db.Column(db.String(255), nullable=False)

class Coleccion(db.Model):
	_tablename__ = 'colecciones'
	id = db.Column(db.Integer, primary_key=True)
	id_libro = db.Column(db.Integer, db.ForeignKey('libros.id'))
	nombre = db.Column(db.String(255), nullable=False)
