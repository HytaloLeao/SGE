from flask import Blueprint, request, jsonify
from models import db, Produto

# Instância (objeto) de Blueprint para produtos
produto_bp = Blueprint('produtos', __name__)

# Rota para criar um novo produto (POST)
@produto_bp.route('/produtos', methods=['POST'])
def criar_produto():
    produto = request.json

    if not produto or 'nome' not in produto or 'preco' not in produto:
        return jsonify({'message': 'Dados inválidos'}), 400

    novo_produto = Produto(produto_nome=produto['nome'], produto_preco=produto['preco'])
    db.session.add(novo_produto)
    db.session.commit()

    return jsonify({'id': novo_produto.produto_id, 'nome': novo_produto.produto_nome, 'preco': str(novo_produto.produto_preco)}), 201

# Rota para listar todos os produtos (GET)
@produto_bp.route('/produtos', methods=['GET'])
def listar_produtos():
    produtos = Produto.query.all()
    return jsonify([{'id': p.produto_id, 'nome': p.produto_nome, 'preco': str(p.produto_preco)} for p in produtos]), 200

# Rota para atualizar um produto existente (PUT)
@produto_bp.route('/produtos/<int:id>', methods=['PUT'])
def atualizar_produto(id):
    data = request.json
    produto = Produto.query.get(id)

    if not produto:
        return jsonify({'message': 'Produto não encontrado'}), 404
    
    if not data or 'nome' not in data or 'preco' not in data:
        return jsonify({'message': 'Dados inválidos'}), 400

    produto.produto_nome = data['nome']
    produto.produto_preco = data['preco']
    db.session.commit()

    return jsonify({'id': produto.produto_id, 'nome': produto.produto_nome, 'preco': str(produto.produto_preco)}), 200

# Rota para deletar um produto existente (DELETE)
@produto_bp.route('/produtos/<int:id>', methods=['DELETE'])
def deletar_produto(id):
    produto = Produto.query.get(id)

    if not produto:
        return jsonify({'message': 'Produto não encontrado'}), 404
    
    db.session.delete(produto)
    db.session.commit()

    return jsonify({'message': 'Produto deletado com sucesso'}), 200