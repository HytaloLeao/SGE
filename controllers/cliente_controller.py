from flask import Blueprint, request, jsonify
from models import db, Cliente

# Instância (objeto) de Blueprint para clientes
cliente_bp = Blueprint('clientes', __name__)

# Rota para criar um novo cliente (POST)
@cliente_bp.route('/clientes', methods=['POST'])
def criar_cliente():
    cliente = request.json

    if not cliente or 'cliente_nome' not in cliente or 'cliente_email' not in cliente:
        return jsonify({'message': 'Dados inválidos'}), 400

    novo_cliente = Cliente(cliente_nome=cliente['cliente_nome'],
                           cliente_email=cliente['cliente_email'])
    db.session.add(novo_cliente)
    db.session.commit()

    return jsonify({'id': novo_cliente.cliente_id, 'nome': novo_cliente.nome, 'email': novo_cliente.email}), 201

# Rota para listar todos os clientes (GET)
@cliente_bp.route('/clientes', methods=['GET'])
def listar_clientes():
    clientes = Cliente.query.all()
    return jsonify([{'id': c.cliente_id, 'nome': c.cliente_nome, 'email': c.cliente_email} for c in clientes]), 200

# Rota para atualizar um cliente existente (PUT)
@cliente_bp.route('/clientes/<int:id>', methods=['PUT'])
def atualizar_cliente(id):
    data = request.json
    cliente = Cliente.query.get(id)

    if not cliente:
        return jsonify({'message': 'Cliente não encontrado'}), 404
    
    if not data or 'nome' not in data or 'email' not in data:
        return jsonify({'message': 'Dados inválidos'}), 400

    cliente.nome = data['nome']
    cliente.email = data['email']
    db.session.commit()

    return jsonify({'id': cliente.cliente_id, 'nome': cliente.nome, 'email': cliente.email}), 200

# Rota para deletar um cliente existente (DELETE)
@cliente_bp.route('/clientes/<int:id>', methods=['DELETE'])
def deletar_cliente(id):
    cliente = Cliente.query.get(id)

    if not cliente:
        return jsonify({'message': 'Cliente não encontrado'}), 404
    
    db.session.delete(cliente)
    db.session.commit()

    return jsonify({'message': 'Cliente deletado com sucesso'}), 200