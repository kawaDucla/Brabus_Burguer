from flask import Blueprint, render_template, session, redirect, request
from models.produto import Produto
from models.pedido import Pedido
from extensions import db

cliente_bp = Blueprint("cliente", __name__)

@cliente_bp.route("/")
def home():
    return render_template("home.html")

@cliente_bp.route("/cardapio")
def cardapio():
    produtos = Produto.query.all()
    return render_template("cliente/cardapio.html", produtos=produtos)


@cliente_bp.route("/add/<int:id>")
def add(id):
    carrinho = session.get("carrinho", {})
    carrinho[str(id)] = carrinho.get(str(id), 0) + 1
    session["carrinho"] = carrinho
    return redirect("/")


@cliente_bp.route("/carrinho")
def carrinho():
    carrinho = session.get("carrinho", {})

    ids = list(map(int, carrinho.keys())) if carrinho else []
    produtos = Produto.query.filter(Produto.id.in_(ids)).all() if ids else []

    total = sum([p.preco * carrinho[str(p.id)] for p in produtos]) if produtos else 0

    return render_template("cliente/carrinho.html", produtos=produtos, carrinho=carrinho, total=total)


@cliente_bp.route("/checkout")
def checkout():
    return render_template("cliente/checkout.html")


@cliente_bp.route("/finalizar", methods=["POST"])
def finalizar():
    carrinho = session.get("carrinho", {})

    ids = list(map(int, carrinho.keys()))
    produtos = Produto.query.filter(Produto.id.in_(ids)).all()

    total = sum([p.preco * carrinho[str(p.id)] for p in produtos])

    pedido = Pedido(
        total=total,
        pagamento=request.form["pagamento"]
    )

    db.session.add(pedido)
    db.session.commit()

    session["carrinho"] = {}

    return "Pedido realizado com sucesso!"