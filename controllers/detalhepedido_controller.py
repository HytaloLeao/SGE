from flask import Blueprint, request, jsonify
from models import db, Pedido, Produto, DetalhePedido

detalhePedido_bp = Blueprint('detalhepedidos', __name__)

@detalhePedido_bp.route('/detalhepedidos', methods=['POST'])
def criar_detalhe_pedidos():

    detalhepedido = request.json

    novo_detalhe_pedido = DetalhePedido(dp_quantidade=detalhepedido['dp_quantidade'],
                                        dp_preco=detalhepedido['dp_preco'],
                                        dp_desconto=detalhepedido['dp_desconto'],
                                        dp_pedido_id=detalhepedido['dp_pedido_id'],
                                        dp_produto_id=detalhepedido['dp_produto_id'])
    
    db.session.add(novo_detalhe_pedido)
    db.session.commit()

    return jsonify({'id': novo_detalhe_pedido.dp_id})