from flask import Blueprint, render_template, request, redirect, session
from models.produto import Produto
from models.pedido import Pedido
from extensions import db
from functools import wraps
from flask import session, redirect
admin_bp = Blueprint("admin", __name__)



def admin_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not session.get("is_admin"):
            return redirect("/login")
        return f(*args, **kwargs)
    return wrapper
def admin_required():
    return session.get("is_admin")


@admin_bp.route("/")
def dashboard():
    if not admin_required():
        return redirect("/login")

    pedidos = Pedido.query.all()
    faturamento = sum([p.total for p in pedidos])

    return render_template("admin/dashboard.html",
                           pedidos=pedidos,
                           faturamento=faturamento)


@admin_bp.route("/produtos", methods=["GET", "POST"])
def produtos():
    if not admin_required():
        return redirect("/login")

    if request.method == "POST":
        p = Produto(
            nome=request.form["nome"],
            descricao=request.form["descricao"],
            preco=float(request.form["preco"])
        )
        db.session.add(p)
        db.session.commit()

    produtos = Produto.query.all()
    return render_template("admin/produtos.html", produtos=produtos)


@admin_bp.route("/pedidos")
def pedidos():
    pedidos = Pedido.query.all()
    return render_template("admin/pedidos.html", pedidos=pedidos)


@admin_bp.route("/pedidos/atualizar/<int:id>", methods=["POST"])
def atualizar(id):
    pedido = Pedido.query.get(id)
    pedido.status = request.form["status"]
    db.session.commit()
    return redirect("/admin/pedidos")