from app.model.dosen import Dosen
from app.model.mahasiswa import Mahasiswa
from app import response, app, db
from flask import jsonify, request
import math


# GET DATA
def index():
    try:
        dosen = Dosen.query.all()
        data = formatArray(dosen)
        return response.success(data, "Success!")
    except Exception as e:
        print(e)

def formatArray(datas):
    array = []

    for i in datas:
        array.append(singleObject(i))

    return array

def singleObject(data):
    data = {
        'id' : data.id,
        'nidn' : data.nidn,
        'nama' : data.nama,
        'phone' : data.phone,
        'alamat' : data.alamat
    }
    return data


# GET DATA BY DETAIL 
def detail(id):
    try:
        dosen = Dosen.query.filter_by(id=id).first()
        mahasiswa = Mahasiswa.query.filter((Mahasiswa.dosen_satu == id) | (Mahasiswa.dosen_dua == id))

        if not dosen:
            return response.badRequest([], 'Tidak ada data dosen!')
        
        dataMahasiswa = formatMahasiswa(mahasiswa)
        data = singleDetailMahasiswa(dosen, dataMahasiswa)

        return response.success(data, "Success!")
    except Exception as e:
        print(e)

def singleDetailMahasiswa(dosen, dataMahasiswa):
    data = {
        'id' : dosen.id,
        'nidn' : dosen.nidn,
        'nama' : dosen.nama,
        'phone' : dosen.phone,
        'alamat' : dosen.alamat,
        'mahasiswa' : dataMahasiswa
    }
    return data

def singleMahasiswa(mahasiswa):
    data = {
        'id' : mahasiswa.id,
        'nim' : mahasiswa.nim,
        'nama' : mahasiswa.nama,
        'phone' : mahasiswa.phone,
    }
    return data

def formatMahasiswa(data):
    array = []

    for i in data:
        array.append(singleMahasiswa(i))
    return array


# POST DATA
def save():
    try:
        nidn = request.form.get('nidn')
        nama = request.form.get('nama')
        phone = request.form.get('phone')
        alamat = request.form.get('alamat')
        
        input = [
            {
                'nidn' : nidn,
                'nama' : nama,
                'phone' : phone,
                'alamat' : alamat,
            }
        ]
        dosens = Dosen(nidn=nidn, nama=nama, phone=phone, alamat=alamat)
        db.session.add(dosens)
        db.session.commit()

        return response.success(input,'Sukses Menambahkan Data!')
    except Exception as e:
        return(e)
    

# UPDATE DATA
def ubah(id):
    try:
        nidn = request.form.get('nidn')
        nama = request.form.get('nama')
        phone = request.form.get('phone')
        alamat = request.form.get('alamat')

        input = [
            {
                'nidn' : nidn,
                'nama' : nama,
                'phone' : phone,
                'alamat' : alamat,
            }
        ]

        dosen = Dosen.query.filter_by(id=id).first()
        
        dosen.nidn = nidn
        dosen.nama = nama
        dosen.phone = phone
        dosen.alamat = alamat

        db.session.commit()

        return response.success(input,'Sukses Edit Data!')
    except Exception as e:
        return(e)
    
def hapus(id):
    try:
        dosen = Dosen.query.filter_by(id=id).first()
        if not dosen:
            return response.badRequest([],'Data dosen kosong....')
        
        db.session.delete(dosen)
        db.session.commit()

        return response.success('','Sukses Hapus Data!')

    except Exception as e:
        print(e)

def get_pagination(clss, url, start, limit):
    # Ambil data
    results = clss.query.all()
    # Ubah format
    data = formatArray(results)
    # Hitung jumlah data
    count = len(data)

    obj = {}

    if count < start:
        obj['success'] = False
        obj['message'] = 'Page yang dipilih melewati batas total data!'
        return obj
    else:
        obj['success'] = True
        obj['start_page'] = start
        obj['per_page'] = limit
        obj['total_data'] = count

        # Previous Link
        if start == 1:
            obj['previous'] = ''
        else:
            start_copy = max(1, start-limit)
            limit_copy = start - 1
            obj['previous'] = url + '?start=%d&limit=%d' % (start_copy, limit_copy)

            # Next Link
        if start + limit > count:
            obj['next'] = ''
        else:
            obj['next'] = url + '?start=%d&limit=%d' % (start_copy, limit)

        obj['results'] = data[(start-1):(start-1+limit)]
        return obj
    
def paginate():
    start = request.args.get('start')
    limit = request.args.get('limit')

    try:
        if start == None or limit == None:
            return jsonify(get_pagination(
                Dosen,
                'http://localhost:5000/api/dosen/page',
                start = request.args.get('start', 1),
                limit = request.args.get('limit', 3)
           ))
        else:
            return jsonify(get_pagination(
                Dosen,
                'http://localhost:5000/api/dosen/page',
                start = int(start),
                limit = int(limit)
            ))
    except Exception as e:
        print(e)