from flask import Blueprint, request, jsonify
from datetime import datetime
from models import db, Pedido

# Instância (objeto) de Blueprint para pedidos
pedido_bp = Blueprint('pedidos', __name__)

# Decorator da rota produtos, que é do tipo POST (enviando dados)
@pedido_bp.route('/pedidos', methods=['POST'])
def criar_pedido():
    
    pedido = request.json

    _data_compra = datetime.strptime(pedido['data_compra'], '%Y-%m-%d').date()

    novo_pedido = Pedido(data_compra=_data_compra,
                           cliente_id=pedido['cliente_id'])
    db.session.add(novo_pedido)
    db.session.commit()
    
    return jsonify({'id': novo_pedido.pedido_id, 'data_compra': novo_pedido.data_compra}), 201

# Rota para listar todos os pedidos (GET)
@pedido_bp.route('/pedidos', methods=['GET'])
def listar_pedidos():
    pedidos = Pedido.query.all()
    return jsonify([{'id': p.pedido_id, 'data_compra': p.data_compra.isoformat(), 'cliente_id': p.cliente_id} for p in pedidos]), 200

# Rota para atualizar um pedido existente (PUT)
@pedido_bp.route('/pedidos/<int:id>', methods=['PUT'])
def atualizar_pedido(id):
    data = request.json
    pedido = Pedido.query.get(id)

    if not pedido:
        return jsonify({'message': 'Pedido não encontrado'}), 404
    
    if not data or 'data_compra' not in data or 'cliente_id' not in data:
        return jsonify({'message': 'Dados inválidos'}), 400

    pedido.data_compra = data['data_compra']
    pedido.cliente_id = data['cliente_id']
    db.session.commit()

    return jsonify({'id': pedido.pedido_id, 'data_compra': pedido.data_compra.isoformat(), 'cliente_id': pedido.cliente_id}), 200

# Rota para deletar um pedido existente (DELETE)
@pedido_bp.route('/pedidos/<int:id>', methods=['DELETE'])
def deletar_pedido(id):
    pedido = Pedido.query.get(id)

    if not pedido:
        return jsonify({'message': 'Pedido não encontrado'}), 404
    
    db.session.delete(pedido)
    db.session.commit()

    return jsonify({'message': 'Pedido deletado com sucesso'}), 200