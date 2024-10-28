from flask import Blueprint, request, jsonify
from models import db, Categoria

# Instância (objeto) de Blueprint para categorias
categoria_bp = Blueprint('categorias', __name__)

# Rota para criar uma nova categoria (POST)
@categoria_bp.route('/categorias', methods=['POST'])
def criar_categoria():
    categoria = request.json

    if not categoria or 'nome_categoria' not in categoria:
        return jsonify({'message': 'Dados inválidos'}), 400

    nova_categoria = Categoria(nome_categoria=categoria['nome_categoria'])
    db.session.add(nova_categoria)
    db.session.commit()

    return jsonify({'id': nova_categoria.id_categoria, 'nome': nova_categoria.nome_categoria}), 201

# Rota para listar todas as categorias (GET)
@categoria_bp.route('/categorias', methods=['GET'])
def listar_categorias():
    categorias = Categoria.query.all()
    return jsonify([{'id': c.id_categoria, 'nome': c.nome_categoria} for c in categorias]), 200

# Rota para atualizar uma categoria existente (PUT)
@categoria_bp.route('/categorias/<int:id>', methods=['PUT'])
def atualizar_categoria(id):
    data = request.json
    categoria = Categoria.query.get(id)

    if not categoria:
        return jsonify({'message': 'Categoria não encontrada'}), 404
    
    if not data or 'nome_categoria' not in data:
        return jsonify({'message': 'Dados inválidos'}), 400

    categoria.nome_categoria = data['nome_categoria']
    db.session.commit()

    return jsonify({'id': categoria.id_categoria, 'nome': categoria.nome_categoria}), 200

# Rota para deletar uma categoria existente (DELETE)
@categoria_bp.route('/categorias/<int:id>', methods=['DELETE'])
def deletar_categoria(id):
    categoria = Categoria.query.get(id)

    if not categoria:
        return jsonify({'message': 'Categoria não encontrada'}), 404
    
    db.session.delete(categoria)
    db.session.commit()

    return jsonify({'message': 'Categoria deletada com sucesso'}), 200