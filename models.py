from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Notes(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(25), default="New Note")
	content = db.Column (db.Text, default=" ")
	notes_notebook = db.Column(db.Integer, nullable=False)
	image = db.Column(db.String(255), nullable=True) #stores image filename
