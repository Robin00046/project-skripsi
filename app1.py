from flask import Flask, g, render_template, request, redirect, session, url_for
import pickle  
import sklearn  
import matplotlib.pyplot as plt
import numpy as np            # numpy==1.19.3  
from flaskext.mysql import MySQL
import pymysql

app = Flask(__name__)
mysql = MySQL()
# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'bdt'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

class User:
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    def __repr__(self):
        return f'<User: {self.username}>'

users = []
users.append(User(id=1, username='admin', password='admin'))


app = Flask(__name__)
app.secret_key = 'somesecretkeythatonlyishouldknow'

@app.before_request
def before_request():
    g.user = None

    if 'user_id' in session:
        user = [x for x in users if x.id == session['user_id']][0]
        g.user = user

@app.route('/', methods=['GET', 'POST'])

def login():
    if g.user:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        session.pop('user_id', None)

        username = request.form['username']
        password = request.form['password']
        
        user = [x for x in users if x.username == username][0]
        if user and user.password == password:
            session['user_id'] = user.id
            return redirect(url_for('index'))
        return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/index')
def index():
    if not g.user:
        return redirect(url_for('login'))
    conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    data=cur.execute('SELECT * FROM bdt')
    print(data)
    cur.close()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    tidak=cur.execute('SELECT * FROM bdt where penerima_pkh=0')
    print(tidak)
    cur.close()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    ya=cur.execute('SELECT * FROM bdt where penerima_pkh=1')
    print(ya)
    cur.close()
    return render_template('index.html', datas=data, tdk=tidak, ya=ya)
@app.route('/about')
def about():
    if not g.user:
        return redirect(url_for('login'))
    return render_template('about.html')
@app.route('/test')
def test():
    conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    cur.execute('SELECT Select Count(*) From bdt')
    data = cur.fetchall()
    cur.close()
    # return render_template('data.html', computers=data)
    penerima_pkh = []
    for i in cur:
        penerima_pkh.append(i[0])

    plt.bar(penerima_pkh, height)
    plt.ylim(300, 2)
# setting xlabel of graph
    plt.xlabel("Name of Students")
 # setting ylabel of graph
    plt.ylabel("Marks of Students")
 # setting tile of graph
    plt.title("Student's Information")
# show() method to display the graph
    plt.show()
    return render_template('test.html', name = plt.show())
    
@app.route('/proses', methods=['POST', 'GET'])
def proses():
    if not g.user:
        return redirect(url_for('login'))
    
    if request.method =='POST' :

        with open('model2.pkl', 'rb') as r:  
         model = pickle.load(r) 
        
        depan = str(request.form['depan'])
        sta_bangunan = int(request.form['sta_bangunan'])  
        sta_lahan = int(request.form['sta_lahan'])  
        luas_lantai = int(request.form['luas_lantai'])  
        lantai = int(request.form['lantai'])  
        dinding = int(request.form['dinding'])  
        kondisi_dinding = int(request.form['kondisi_dinding'])  
        atap = int(request.form['atap'])  
        kondisi_atap = int(request.form['kondisi_atap'])  
        sumber_airminum = int(request.form['sumber_airminum'])
        cara_peroleh_airminum = int(request.form['cara_peroleh_airminum'])
        ibu_hamil = int(request.form['ibu_hamil'])
        anak_sekolah = int(request.form['anak_sekolah'])
        balita = int(request.form['balita'])
        lansia = int(request.form['lansia'])

        datas = np.array((sta_bangunan,sta_lahan,luas_lantai,lantai,dinding,kondisi_dinding,atap,kondisi_atap,sumber_airminum,cara_peroleh_airminum,ibu_hamil,anak_sekolah,balita,lansia))  
        datas = np.reshape(datas, (1, -1))  
   
        Kelayakan = model.predict(datas)  
    
        return render_template('hasil.html', finalData=Kelayakan, nama=depan) 
    else:
        return render_template('proses.html')



@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))
#crud
@app.route('/data')
def data():
    if not g.user:
        return redirect(url_for('login'))
    conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    cur.execute('SELECT * FROM bdt')
    data = cur.fetchall()
    cur.close()
    return render_template('data.html', computers=data)

@app.route('/tambah')
def tambah():
    if not g.user:
        return redirect(url_for('login'))
    return render_template('tambah.html')

@app.route('/simpan', methods=['POST'])
def simpan():
    conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    if request.method == 'POST':
        id = request.form['id']
        id_bdt = request.form['id_bdt']
        nama_krt = request.form['nama_krt']
        sta_bangunan = request.form['sta_bangunan']
        sta_lahan = request.form['sta_lahan']
        luas_lantai = request.form['luas_lantai']
        lantai = request.form['lantai']
        dinding = request.form['dinding']
        kondisi_dinding = request.form['kondisi_dinding']
        atap = request.form['atap']
        kondisi_atap = request.form['kondisi_atap']
        sumber_airminum = request.form['sumber_airminum']
        cara_peroleh_airminum = request.form['cara_peroleh_airminum']
        ibu_hamil = request.form['ibu_hamil']
        anak_sekolah = request.form['anak_sekolah']
        balita = request.form['balita']
        lansia = request.form['lansia']
        penerima_pkh = request.form['penerima_pkh']
        cur.execute("INSERT INTO bdt (id,id_bdt, nama_krt, sta_bangunan ,sta_lahan ,luas_lantai ,lantai,dinding,kondisi_dinding,atap,kondisi_atap,sumber_airminum,cara_peroleh_airminum,ibu_hamil,anak_sekolah,balita,lansia,penerima_pkh) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", (id, id_bdt, nama_krt, sta_bangunan ,sta_lahan ,luas_lantai ,lantai,dinding,kondisi_dinding,atap,kondisi_atap,sumber_airminum,cara_peroleh_airminum,ibu_hamil,anak_sekolah,balita,lansia,penerima_pkh))
        conn.commit()
        return redirect(url_for('data'))

@app.route('/edit/<id>', methods = ['POST', 'GET'])
def get_data(id):
    conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    cur.execute('SELECT * FROM bdt WHERE id = %s', (id))
    data = cur.fetchall()
    cur.close()
    print(data[0])
    return render_template('edit.html', computers = data[0])

@app.route('/update/<id>', methods=['POST'])
def update(id):
    if request.method == 'POST':
        id_bdt = request.form['id_bdt']
        nama_krt = request.form['nama_krt']
        sta_bangunan = request.form['sta_bangunan']
        sta_lahan = request.form['sta_lahan']
        luas_lantai = request.form['luas_lantai']
        lantai = request.form['lantai']
        dinding = request.form['dinding']
        kondisi_dinding = request.form['kondisi_dinding']
        atap = request.form['atap']
        kondisi_atap = request.form['kondisi_atap']
        sumber_airminum = request.form['sumber_airminum']
        cara_peroleh_airminum = request.form['cara_peroleh_airminum']
        ibu_hamil = request.form['ibu_hamil']
        anak_sekolah = request.form['anak_sekolah']
        balita = request.form['balita']
        lansia = request.form['lansia']
        penerima_pkh = request.form['penerima_pkh']
        conn = mysql.connect()
        cur = conn.cursor(pymysql.cursors.DictCursor)
        cur.execute(" UPDATE bdt SET id_bdt = %s ,nama_krt = %s,sta_bangunan = %s,sta_lahan = %s,luas_lantai = %s,lantai = %s,dinding = %s,kondisi_dinding = %s,atap = %s,kondisi_atap = %s,sumber_airminum = %s,cara_peroleh_airminum = %s,ibu_hamil = %s,anak_sekolah = %s,balita = %s,lansia = %s,penerima_pkh  = %s  WHERE id = %s ", (id_bdt, nama_krt, sta_bangunan ,sta_lahan ,luas_lantai ,lantai,dinding,kondisi_dinding,atap,kondisi_atap,sumber_airminum,cara_peroleh_airminum,ibu_hamil,anak_sekolah,balita,lansia,penerima_pkh,id))
        conn.commit()
        return redirect(url_for('data'))

@app.route('/delete/<string:id>', methods = ['GET'])
def delete(id):
    conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    cur.execute('DELETE FROM bdt WHERE id = {0}'.format(id))
    conn.commit()
    return redirect(url_for('data'))


if __name__ == "__main__":
    app.run(debug=True)