import _sqlite3 as sql
from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.exceptions import abort

app = Flask(__name__)
app.config['SECRET_KEY'] = 'J@v@Dev23'

def db_connection():
    conn = sql.connect("filmflix.db")
    conn.row_factory = sql.Row
    return conn

def get_film(film_ID):
    conn = db_connection()
    film = conn.execute('SELECT * FROM tblFilms WHERE filmID = ?',
                        (film_ID,)).fetchall()
    conn.close()
    if film is None:
        abort(404)
    return (film)

@app.route('/')
def index():
    conn = db_connection()
    films = conn.execute('SELECT * FROM tblFilms').fetchall()
    conn.close()
    return render_template('index.html', films=films)

@app.route('/<int:film_ID>')
def find_film(film_ID):
    film = get_film(film_ID)
    return render_template('film.html', film=film)

@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        yearReleased = request.form['yearReleased']
        rating = request.form['rating']
        duration = request.form['duration']
        genre = request.form['genre']

        if not title:
            flash('Title is required!')
        else:
            conn = db_connection()
            conn.execute('INSERT INTO tblFilms (title, yearReleased, rating, duration, genre) VALUES (?, ?, ?, ?, ?)',
                         (title, yearReleased, rating, duration, genre))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))
        
    return render_template('create.html')

@app.route('/<int:id>/edit', methods=('GET','POST'))
def edit(id):
    post = get_film(id)

    if request.method == 'POST':
        title = request.form['title']
        yearReleased = request.form['yearReleased']
        rating = request.form['rating']
        duration = request.form['duration']
        genre = request.form['genre']

        if not title:
            flash('Title is required!')
        else:
            conn = db_connection()
            conn.execute('UPDATE tblFilms SET title = ?, yearReleased = ?, rating = ?, duration = ?, genre = ?'
                         'WHERE filmID = ?',
                         (title, yearReleased, rating, duration, genre, id))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('edit.html', post=post)

@app.route('/<int:id>/delete', methods=('POST',))
def delete(id):
    post = get_film(id)
    conn = db_connection()
    conn.execute('DELETE FROM tblFilms WHERE filmID = ?', (id,))
    conn.commit()
    conn.close()
    flash('"{}" was successfully deleted!'.format(post['title']))
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=5000)

