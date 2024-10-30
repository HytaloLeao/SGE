from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, create_access_token
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
@jwt_required()  # Protege a rota
def listar_usuarios():
    usuarios = Usuario.query.all()
    return jsonify([{'id': u.usuario_id, 'login': u.usuario_login, 'senha': u.usuario_senha} for u in usuarios]), 200

# Rota para atualizar um usuário existente (PUT)
@usuario_bp.route('/usuarios/<int:id>', methods=['PUT'])
@jwt_required()  # Protege a rota
def atualizar_usuario(id):
    data = request.json
    usuario = Usuario.query.get(id)

    if not usuario:
        return jsonify({'message': 'Usuário não encontrado'}), 404
    
    if not data or 'usuario_login' not in data or 'usuario_senha' not in data:
        return jsonify({'message': 'Dados inválidos'}), 400

    usuario.usuario_login = data['usuario_login']
    usuario.usuario_senha = data['usuario_senha']
    db.session.commit()

    return jsonify({'id': usuario.usuario_id, 'login': usuario.usuario_login, 'senha': usuario.usuario_senha}), 200

# Rota para deletar um usuário existente (DELETE)
@usuario_bp.route('/usuarios/<int:id>', methods=['DELETE'])
@jwt_required()  # Protege a rota
def deletar_usuario(id):
    usuario = Usuario.query.get(id)

    if not usuario:
        return jsonify({'message': 'Usuário não encontrado'}), 404
    
    db.session.delete(usuario)
    db.session.commit()

    return jsonify({'message': 'Usuário deletado com sucesso'}), 200

# Rota para login (POST)
@usuario_bp.route('/login', methods=['POST'])
def login():
    username = request.json.get('usuario')
    password = request.json.get('senha')

    # Verificar se o usuário existe e a senha está correta
    usuario = Usuario.query.filter_by(usuario_login=username).first()
    if not usuario or usuario.usuario_senha != password:
        return jsonify({'msg': 'Usuário ou senha incorretos'}), 401
    
    # Criar um token JWT para o usuário
    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token), 200