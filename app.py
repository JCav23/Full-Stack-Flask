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
        poster = request.form['poster']

        if not title:
            flash('Title is required!')
        else:
            conn = db_connection()
            conn.execute('INSERT INTO tblFilms (title, yearReleased, rating, duration, genre, poster) VALUES (?, ?, ?, ?, ?)',
                         (title, yearReleased, rating, duration, genre, poster))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))
        
    return render_template('create.html')

@app.route('/<int:fID>/edit', methods=('GET','POST'))
def edit(fID):
    post = get_film(fID)
    heading = get_film(fID)[0][1]

    if request.method == 'POST':
        title = request.form.get('title')
        yearReleased = request.form.get('yearReleased')
        rating = request.form.get('rating')
        duration = request.form.get('duration')
        genre = request.form.get('genre')
        poster = request.form.get('poster')

        if not title:
            flash('Title is required!')
        else:
            conn = db_connection()
            conn.execute('UPDATE tblFilms SET title = ?, yearReleased = ?, rating = ?, duration = ?, genre = ?, poster = ? WHERE filmID = ?',
                         (title, yearReleased, rating, duration, genre, poster, fID))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('edit.html', post=post, heading=heading)

@app.route('/<int:fID>/delete', methods=['POST'])
def delete(fID):
     if request.method == 'POST':
        post = get_film(fID)[0][1]
        conn = db_connection()
        conn.execute('DELETE FROM tblFilms WHERE filmID = ?', (fID,))
        conn.commit()
        conn.close()
        flash(f'Entry: {post} was successfully deleted!')
        return redirect(url_for('index'))
     
@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        search = request.form['search']
        conn = db_connection()
        results = conn.execute('SELECT * FROM tblFilms WHERE title LIKE % OR yearReleased LIKE % OR rating LIKE % OR duration LIKE % OR genre LIKE %', (search)).fetchall()
        conn.close()
        return redirect(url_for('search'))


if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=5000)

