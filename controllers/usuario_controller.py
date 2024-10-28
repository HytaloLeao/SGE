from flask import Blueprint, request, jsonify
from models import db, Usuario

# Instância (objeto) de Blueprint para usuários
usuario_bp = Blueprint('usuarios', __name__)

# Rota para criar um novo usuário (POST)
@usuario_bp.route('/usuarios', methods=['POST'])
def criar_usuario():
    usuario = request.json

    if not usuario or 'usuario_login' not in usuario or 'usuario_senha' not in usuario:
        return jsonify({'message': 'Dados inválidos'}), 400

    novo_usuario = Usuario(usuario_login=usuario['usuario_login'], usuario_senha=usuario['usuario_senha'])
    db.session.add(novo_usuario)
    db.session.commit()

    return jsonify({'id': novo_usuario.usuario_id, 'login': novo_usuario.usuario_login}), 201

# Rota para listar todos os usuários (GET)
@usuario_bp.route('/usuarios', methods=['GET'])
def listar_usuarios():
    usuarios = Usuario.query.all()
    return jsonify([{'id': u.usuario_id, 'login': u.usuario_login, 'senha': u.usuario_senha} for u in usuarios]), 200

# Rota para atualizar um usuário existente (PUT)
@usuario_bp.route('/usuarios/<int:id>', methods=['PUT'])
def atualizar_usuario(id):
    data = request.json
    usuario = Usuario.query.get(id)

    if not usuario:
        return jsonify({'message': 'Usuário não encontrado'}), 404
    
    if not data or 'login' not in data or 'senha' not in data:
        return jsonify({'message': 'Dados inválidos'}), 400

    usuario.usuario_login = data['login']
    usuario.usuario_senha = data['senha']
    db.session.commit()

    return jsonify({'id': usuario.usuario_id, 'login': usuario.usuario_login, 'senha': usuario.usuario_senha}), 200

# Rota para deletar um usuário existente (DELETE)
@usuario_bp.route('/usuarios/<int:id>', methods=['DELETE'])
def deletar_usuario(id):
    usuario = Usuario.query.get(id)

    if not usuario:
        return jsonify({'message': 'Usuário não encontrado'}), 404
    
    db.session.delete(usuario)
    db.session.commit()

    return jsonify({'message': 'Usuário deletado com sucesso'}), 200