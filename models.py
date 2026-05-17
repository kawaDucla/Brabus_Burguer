from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Produto(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    nome = db.Column(db.String(100), nullable=False)

    descricao = db.Column(db.String(255), nullable=False)

    preco = db.Column(db.Float, nullable=False)

    imagem = db.Column(db.String(255), nullable=True)

    categoria = db.Column(db.String(50), nullable=True)

    def __repr__(self):
        return f'<Produto {self.nome}>'
    