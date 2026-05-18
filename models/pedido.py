from extensions import db

class Pedido(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    total = db.Column(db.Float)
    pagamento = db.Column(db.String(30))
    status = db.Column(db.String(30), default="recebido")