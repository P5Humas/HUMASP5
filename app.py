import sqlite3
from flask import Flask, render_template, g, jsonify, request, send_from_directory, redirect, url_for, session
import json  # Untuk mengubah data menjadi JSON
import os
from werkzeug.utils import secure_filename
import secrets



app = Flask(__name__)
app.secret_key = secrets.token_hex(16)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'jpg', 'jpeg', 'png', 'gif', 'mp4', 'mov'}
app.config['MAX_CONTENT_LENGTH'] = 200 * 1024 * 1024  # 200 MB/etc/nginx/nginx.conf


DATABASE = 'humas.db'

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# Buat folder untuk menyimpan file upload jika belum ada
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# Fungsi untuk mendapatkan koneksi database
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row  # Agar hasil query berupa dictionary
    return db

# Fungsi untuk melakukan query pada database
def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

# Fungsi untuk menutup koneksi database
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

# Route utama (untuk menampilkan grafik di halaman web)
@app.route('/')
def index():
    return render_template('landingPage/dashboard.html')
# API untuk mendapatkan data chart1 (jumlah murid per bulan)
@app.route('/api/chart1', methods=['GET'])
def get_chart1_data():
    query = """
        SELECT bulan, status, SUM(jumlah) AS jumlah
        FROM murid
        GROUP BY bulan, status
        ORDER BY CASE
            WHEN bulan = 'Jan' THEN 1
            WHEN bulan = 'Feb' THEN 2
            WHEN bulan = 'Mar' THEN 3
            WHEN bulan = 'Apr' THEN 4
            WHEN bulan = 'Mei' THEN 5
            WHEN bulan = 'Jun' THEN 6
            WHEN bulan = 'Jul' THEN 7
            WHEN bulan = 'Agu' THEN 8
            WHEN bulan = 'Sep' THEN 9
            WHEN bulan = 'Okt' THEN 10
            WHEN bulan = 'Nov' THEN 11
            WHEN bulan = 'Des' THEN 12
        END
    """
    data = query_db(query)

    # Inisialisasi data chart1
    chart1_data = {month: {"pkl": 0, "belum-pkl": 0} for month in ["Jan", "Feb", "Mar", "Apr", "Mei", "Jun", "Jul", "Agu", "Sep", "Okt", "Nov", "Des"]}

    # Memproses hasil query untuk chart1
    for row in data:
        bulan = row['bulan']
        status = row['status']
        jumlah = row['jumlah']
        if status == 'pkl':
            chart1_data[bulan]["pkl"] += jumlah
        elif status == 'belum-pkl':
            chart1_data[bulan]["belum-pkl"] += jumlah

    # Sort months manually to ensure correct order
    month_order = ["Jan", "Feb", "Mar", "Apr", "Mei", "Jun", "Jul", "Agu", "Sep", "Okt", "Nov", "Des"]
    sorted_chart1_data = {month: chart1_data[month] for month in month_order}

    return jsonify(sorted_chart1_data)


# API untuk mendapatkan data chart2 (jumlah murid per status)
@app.route('/api/chart2', methods=['GET'])
def get_chart2_data():
    query = """
        SELECT bulan, status, SUM(jumlah) AS jumlah
        FROM murid
        GROUP BY bulan, status
    """
    data = query_db(query)

    # Inisialisasi data chart2
    chart2_data = {"PKL": 0, "Pra PKL": 0, "Belum PKL": 0}

    # Memproses hasil query untuk chart2
    for row in data:
        status = row['status']
        jumlah = row['jumlah']
        if status == 'pkl':
            chart2_data["PKL"] += jumlah
        elif status == 'pra-pkl':
            chart2_data["Pra PKL"] += jumlah
        elif status == 'belum-pkl':
            chart2_data["Belum PKL"] += jumlah

    return jsonify(chart2_data)

# Route untuk halaman BKK
@app.route('/bkk')
def bkk():
    return render_template('bkk.html')
@app.route('/api/lowongan', methods=['GET'])
def get_lowongan_data():
    query = """
        SELECT bulan, jumlah_lowongan
        FROM lowongan
    """
    data = query_db(query)

    # Create a dictionary to store the data
    chart_data = {month: 0 for month in ["Jan", "Feb", "Mar", "Apr", "Mei", "Jun", "Jul", "Agu", "Sep", "Okt", "Nov", "Des"]}

    # Fill the dictionary with the data from the query
    for row in data:
        bulan = row['bulan']
        jumlah = row['jumlah_lowongan']
        chart_data[bulan] = jumlah

    # Sort the chart data to ensure the correct order
    month_order = ["Jan", "Feb", "Mar", "Apr", "Mei", "Jun", "Jul", "Agu", "Sep", "Okt", "Nov", "Des"]
    sorted_chart_data = {month: chart_data[month] for month in month_order}

    return jsonify(sorted_chart_data)
@app.route('/api/alumni', methods=['GET'])
def get_alumni_data():
    query = """
        SELECT bulan, status, SUM(jumlah) AS jumlah
        FROM alumni
        GROUP BY bulan, status
        ORDER BY CASE
            WHEN bulan = 'Jan' THEN 1
            WHEN bulan = 'Feb' THEN 2
            WHEN bulan = 'Mar' THEN 3
            WHEN bulan = 'Apr' THEN 4
            WHEN bulan = 'Mei' THEN 5
            WHEN bulan = 'Jun' THEN 6
            WHEN bulan = 'Jul' THEN 7
            WHEN bulan = 'Agu' THEN 8
            WHEN bulan = 'Sep' THEN 9
            WHEN bulan = 'Okt' THEN 10
            WHEN bulan = 'Nov' THEN 11
            WHEN bulan = 'Des' THEN 12
        END
    """
    data = query_db(query)

    # Inisialisasi data untuk grafik
    chart_data = {month: {"kerja": 0, "belum-kerja": 0} for month in ["Jan", "Feb", "Mar", "Apr", "Mei", "Jun", "Jul", "Agu", "Sep", "Okt", "Nov", "Des"]}

    # Memproses hasil query
    for row in data:
        bulan = row['bulan']
        status = row['status']
        jumlah = row['jumlah']
        if status == 'kerja':
            chart_data[bulan]["kerja"] += jumlah
        elif status == 'belum-kerja':
            chart_data[bulan]["belum-kerja"] += jumlah

    # Sort data berdasarkan urutan bulan
    month_order = ["Jan", "Feb", "Mar", "Apr", "Mei", "Jun", "Jul", "Agu", "Sep", "Okt", "Nov", "Des"]
    sorted_chart_data = {month: chart_data[month] for month in month_order}

    return jsonify(sorted_chart_data)



# Route untuk halaman Sosial
@app.route('/sosial')
def sosial():
    return render_template('sosial.html')

@app.route('/admin/dashboard')
def admin_dashboard():
    return render_template('admin/dashboard.html')
@app.route('/admin/general')
def general_dashboard():
    return render_template('admin/general.html')
@app.route('/admin/sosial')
def sosial_dashboard():
    return render_template('admin/sosial.html')
@app.route('/admin/chart2')
def chart2_dashboard():
    return render_template('admin/chart2.html')

@app.route('/admin/chart1')
def chart1_dashboard():
    return render_template('admin/chart1.html')

@app.route('/landingPage/dashboard')
def landing_dashboard():
    return render_template('landingPage/dashboard.html')
@app.route('/gallery')
def gallery():
    # Ambil data dari tabel 'galery'
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM galery')
    gallery_items = cursor.fetchall()  # Ambil semua data
    conn.close()

    # Kirim data ke template
    return render_template('landingPage/dashboard.html', gallery_items=gallery_items)
@app.route('/api/gallery', methods=['GET'])
def api_gallery():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM galery')
    gallery_items = cursor.fetchall()
    conn.close()

    # Ubah data ke format yang sesuai untuk JSON
    gallery_list = []
    for item in gallery_items:
        gallery_list.append({
            'id_galery': item['id_galery'],
            'url': item['url'],
            'category': item['category']
        })

    return jsonify(gallery_list)

@app.route('/update', methods=['POST'])
def update_jumlah():
    # Ambil data dari request
    category = request.form.get('category')  # Kategori yang dipilih (murid/alumni)
    jumlah = request.form.get('jumlah')  # Jumlah yang dimasukkan
    bulan = request.form.get('bulan')  # Bulan yang dimasukkan
    status = request.form.get('status')  # Status yang dimasukkan

    if category not in ['murid', 'alumni']:
        return jsonify({'error': 'Kategori tidak valid'}), 400

    # Tentukan nama tabel berdasarkan kategori
    table = 'murid' if category == 'murid' else 'alumni'

    # Tambahkan jumlah di tabel yang sesuai
    conn = get_db()
    cursor = conn.cursor()

    # Insert data baru
    cursor.execute(f"INSERT INTO {table} (jumlah, bulan, status) VALUES (?, ?, ?)", (jumlah, bulan, status))

    conn.commit()
    conn.close()

    return jsonify({'message': 'Data berhasil ditambahkan'}), 200


@app.route('/api/aluni', methods=['GET'])
def get_alumni():
    # Mendapatkan tahun yang diminta dari query string, jika ada
    tahun_dipilih = request.args.get('tahun', default=None, type=int)

    # Query untuk mengambil data per tahun
    query = """
        SELECT bulan AS tahun, status, SUM(jumlah) AS jumlah
        FROM alumni
        {}
        GROUP BY tahun, status
        ORDER BY tahun DESC
    """
    
    # Jika tahun dipilih, filter berdasarkan tahun
    if tahun_dipilih:
        query = query.format(f"WHERE bulan = {tahun_dipilih}")
    else:
        query = query.format("")

    data = query_db(query)

    # Inisialisasi data untuk grafik
    chart_data = {}

    # Memproses hasil query
    for row in data:
        tahun = row['tahun']
        status = row['status']
        jumlah = row['jumlah']

        if tahun not in chart_data:
            chart_data[tahun] = {"kerja": 0, "belum-kerja": 0}

        if status == 'kerja':
            chart_data[tahun]["kerja"] += jumlah
        elif status == 'belum-kerja':
            chart_data[tahun]["belum-kerja"] += jumlah

    # Urutkan berdasarkan tahun secara menurun
    sorted_chart_data = {tahun: chart_data[tahun] for tahun in sorted(chart_data.keys(), reverse=True)}

    return jsonify(sorted_chart_data)

@app.route('/api/media', methods=['GET'])
def get_media():
    filter_type = request.args.get('type', 'all')  # Default ke 'all' jika type tidak ada
    print(f"Filtering media by type: {filter_type}")  # Debugging: melihat filter yang diterima

    conn = get_db()
    cursor = conn.cursor()

    if filter_type == 'all':
        cursor.execute("SELECT * FROM galery")
    else:
        cursor.execute("SELECT * FROM galery WHERE category = ?", (filter_type,))

    media = cursor.fetchall()
    conn.close()

    # Mengembalikan hasil sebagai JSON
    return jsonify([dict(row) for row in media])
@app.route('/delete', methods=['POST'])
def delete_data():
    data = request.form
    category = data.get('category')
    status = data.get('status')
    bulan = data.get('bulan')

    conn = get_db()
    cursor = conn.cursor()

    if category == 'jumlah_siswa':
        cursor.execute('DELETE FROM murid WHERE status = ? AND bulan = ?', (status, bulan))
    elif category == 'jumlah_alumni':
        cursor.execute('DELETE FROM alumni WHERE status = ? AND bulan = ?', (status, bulan))
    else:
        return jsonify({'error': 'Kategori tidak valid'}), 400

    conn.commit()
    conn.close()

    return jsonify({'message': 'Data berhasil dihapus'})
@app.route('/updatemurid', methods=['POST'])
def update_data():
    data = request.form
    pkl_status = data.get('pklStatus')  # Status PKL yang baru
    pkl_month = data.get('pklMonth')  # Bulan yang dipilih
    pkl_count = data.get('pklCount')  # Jumlah PKL yang baru

    # Validasi input
    if not pkl_status or not pkl_month or not pkl_count:
        return jsonify({'error': 'Semua field harus diisi'}), 400

    # Membuka koneksi ke database
    conn = get_db()
    cursor = conn.cursor()

    # Mengupdate data di tabel murid berdasarkan bulan dan status
    if pkl_status == 'pkl':
        cursor.execute('''
            UPDATE murid
            SET  jumlah = ?
            WHERE bulan = ? AND status = 'pkl'
        ''', (pkl_count, pkl_month))
    elif pkl_status == 'belum-pkl':
        cursor.execute('''
            UPDATE murid
            SET jumlah = ?
            WHERE bulan = ? AND status = 'belum-pkl'
        ''', (pkl_count, pkl_month))
    else:
        return jsonify({'error': 'Status tidak valid'}), 400

    # Commit perubahan dan menutup koneksi
    conn.commit()
    conn.close()

    # Mengembalikan respon sukses
    return redirect(url_for('chart1_dashboard'))

@app.route('/updatealumni', methods=['POST'])
def update_data_alumni():
    data = request.form
    alumni_status = data.get('Status')  # Status PKL yang baru
    alumni_month = data.get('YearCount')  # Bulan yang dipilih
    alumni_count = data.get('Jumlah')  # Jumlah PKL yang baru

    # Validasi input
    if not alumni_status or not alumni_month or not alumni_count:
        return jsonify({'error': 'Semua field harus diisi'}), 400

    # Membuka koneksi ke database
    conn = get_db()
    cursor = conn.cursor()

    # Mengupdate data di tabel murid berdasarkan bulan dan status
    if alumni_status == 'kerja':
        cursor.execute('''
            UPDATE alumni
            SET  jumlah = ?
            WHERE bulan = ? AND status = 'kerja'
        ''', (alumni_count, alumni_month))
    elif alumni_status == 'belum-kerja':
        cursor.execute('''
            UPDATE alumni
            SET jumlah = ?
            WHERE bulan = ? AND status = 'belum-kerja'
        ''', (alumni_count, alumni_month))
    else:
        return jsonify({'error': 'Status tidak valid'}), 400

    # Commit perubahan dan menutup koneksi
    conn.commit()
    conn.close()

    # Mengembalikan respon sukses
    return redirect(url_for('chart2_dashboard'))

@app.route('/insertlowongan', methods=['POST'])
def insert_lowongan():
    if request.method == 'POST':
        pkl_month = request.form['pklMonth']
        student_count = request.form['studentCount']

        # Simpan data ke database
        conn = get_db()
        conn.execute(
            'INSERT INTO lowongan (bulan, jumlah_lowongan) VALUES (?, ?)',
            (pkl_month, student_count)
        )
        conn.commit()
        conn.close()

        

        return redirect(url_for('chart2_dashboard'))

@app.route('/updatelowongan', methods=['POST'])
def update_lowongan():
    if request.method == 'POST':
        pkl_month = request.form['pklMonth']
        student_count = request.form['studentCount']

        # Update data di database
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(
            'UPDATE lowongan SET jumlah_lowongan = ? WHERE bulan = ?',
            (student_count, pkl_month)
        )
        conn.commit()
        conn.close()

        # Arahkan pengguna ke halaman chart2_dashboard setelah update
        return redirect(url_for('chart2_dashboard'))
@app.route('/api/media/<int:id>', methods=['PUT'])
def edit_media(id):
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        file_url = f'/uploads/{filename}'
        
        category = request.form.get('category')

        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('UPDATE galery SET url = ?, category = ? WHERE id_galery = ?', (file_url, category, id))
        conn.commit()
        conn.close()

        return redirect(url_for('sosial_dashboard'))

    return jsonify({'error': 'File type not allowed'}), 400
@app.route('/api/media/<int:id>', methods=['DELETE'])
def delete_media(id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM galery WHERE id_galery = ?', (id,))
    conn.commit()
    conn.close()
    
    return redirect(url_for('sosial_dashboard'))

@app.route('/api/galery', methods=['POST'])
def add_to_galery():
    # Check if the 'icon' is a file or an SVG URL
    icon = request.form.get('icon')  # This will get the icon URL if provided
    if icon:  # If an SVG link is provided
        if not icon.endswith('.svg'):  # Ensure it's a valid SVG link
            return jsonify({"error": "Invalid SVG link"}), 400

        # Directly save the SVG link to the database
        category = request.form['category']
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO galery (url, category) VALUES (?, ?)', (icon, category))
        conn.commit()
        conn.close()

        return jsonify({"message": "SVG link added to gallery", "icon_url": icon}), 201

    # Handle file upload if no SVG link is provided
    if 'icon' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['icon']
    
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file and allowed_file(file.filename):
        # Using secure_filename to ensure safe file names
        filename = secure_filename(file.filename)
        
        # Set file save path
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        # Save the file to uploads folder
        file.save(filepath)

        # Get category from the form
        category = request.form['category']

        # Construct the file URL
        file_url = f'/uploads/{filename}'

        # Save file URL and category to the database
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO galery (url, category) VALUES (?, ?)', (file_url, category))
        conn.commit()
        conn.close()

        return redirect(url_for('general_dashboard'))
    else:
        return jsonify({"error": "Invalid file type"}), 400

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')


@app.route('/loginproses', methods=['POST'])
def loginproses():
    try:
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']

            conn = get_db()
            guru = conn.execute('SELECT * FROM guru WHERE nama = ? AND password = ?', (username, password)).fetchone()
            conn.close()

            if guru:
                session['logged_in'] = True
                session['username'] = guru['nama']
                return redirect(url_for('admin_dashboard'))
            else:
                return render_template('login.html', error='Invalid username or password')
    except Exception as e:
        return str(e)  # Menampilkan kesalahan jika ada

if __name__ == '__main__':
    app.run(debug=True)
