
from app.model.user import User
from app.model.gambar import Gambar
import datetime

from app import response, app, db, uploadconfig
from flask import request
from flask_jwt_extended import *
import uuid
import os
from werkzeug.utils import secure_filename

def upload():
    try:
        judul = request.form.get('judul')

        if 'file' not in request.files:
            return response.badRequest([],'File tidak tersedia!')
        file = request.files['file']

        if file.filename == '':
            return response.badRequest([],'File tidak tersedia!')
        
        if file and uploadconfig.allowed_file(file.filename):
            uid = uuid.uuid4()
            filename = secure_filename(file.filename)
            renamefile = 'Flask_'+str(uid)+filename

            file.save(os.path.join(app.config['UPLOAD_FOLDER'], renamefile))

            uploads = Gambar(judul=judul, pathname=renamefile)
            db.session.add(uploads)
            db.session.commit()

            return response.success({
                'judul' : judul,
                'pathname' : renamefile
            },
            'Sukses upload file!')
        else:
            return response.badRequest([],'File tidak diizinkan!')

    except Exception as e:
        print(e)



# POST DATA
def buatAdmin():
    try:
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        level = 1

        users = User(name=name, email=email, level=level)
        users.setPassword(password)
        db.session.add(users)
        db.session.commit()

        return response.success('','Sukses Menambahkan Data!')
    except Exception as e:
        return(e)
    
def singleObject(data):
    data = {
        'id' : data.id,
        'name' : data.name,
        'email' : data.email,
        'level' : data.level,
    }

    return data

def login():
    try:
        email = request.form.get('email')
        password = request.form.get('password')
    
        user = User.query.filter_by(email=email).first()

        if not user:
            return response.badRequest([],'Email tidak ditemukan!')

        if not user.checkPassword(password):
            return response.badRequest([],'Password Salah!')

        data = singleObject(user)

        expires = datetime.timedelta(days=7)
        expires_refresh = datetime.timedelta(days=7)

        access_token = create_access_token(data, fresh=True, expires_delta=expires)
        refresh_token = create_refresh_token(data, expires_delta=expires_refresh)

        return response.success({
            'data' : data,
            'access_token' : access_token,
            'refresh_token' : refresh_token
        },'Sukses login!')
    except Exception as e:
        print(e)