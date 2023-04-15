from app import app, response
from app.controller import DosenController
from app.controller import UserController
from flask import request
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required

@app.route('/')
def index():
    return "Hello World"

@app.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return response.success(current_user, 'Sukses!')

@app.route('/file-upload', methods=['GET', 'POST'])
def fileUploads():
    return UserController.upload()

@app.route('/dosen', methods=['GET', 'POST'])
def dosens():
    if request.method == 'GET':
        return DosenController.index()
    else:
        return DosenController.save()

@app.route('/api/dosen/page', methods=['GET'])
def pagination():
    return DosenController.paginate()

@app.route('/dosen/<id>', methods=['GET', 'PUT','DELETE'])
def detailDosen(id):
    if request.method == 'GET':
        return DosenController.detail(id)
    elif request.method == 'PUT':
        return DosenController.ubah(id)
    elif request.method == 'DELETE':
        return DosenController.hapus(id)
    
@app.route('/createadmin', methods=['POST'])
def admins():
    return UserController.buatAdmin()

@app.route('/login', methods=['POST'])
def logins():
    return UserController.login()