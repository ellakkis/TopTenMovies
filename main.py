from flask_bootstrap import Bootstrap
from flask import Flask, render_template, request, url_for, redirect
import os, requests

from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from sqlalchemy import select, desc
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from movie import Movie, db

app = Flask(__name__)

app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
basedir = os.path.abspath(os.path.dirname(__file__))
bootstrap = Bootstrap(app)


app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///top_movies.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.app_context().push() # To solve RuntimeError: Working outside of application context
db.init_app(app)

movies = Movie()

# the movies database api
TMDB_API_KEY = 'b230e8bb3954b64ab516ac13ff23635f'
TMDB_ENDPOINT = 'https://api.themoviedb.org/3/search/movie?'


class MovieForm(FlaskForm):
    title = StringField('title', validators=[DataRequired()])
    submit = SubmitField('Submit')


def tmdb_find_movie(title):
    TMDB_PARAMS = {
        'api_key': TMDB_API_KEY,
        'query': title
    }
    response = requests.get(url=TMDB_ENDPOINT, params=TMDB_PARAMS)
    return response.json()


def tmdb_find_movie_details(movie_id):
    TMDB_ENDPOINT_DETAILS = 'https://api.themoviedb.org/3/movie/'+f'{movie_id}?'
    TMDB_PARAMS = {'api_key': TMDB_API_KEY}
    response = requests.get(url=TMDB_ENDPOINT_DETAILS, params=TMDB_PARAMS)
    return response.json()


@app.route("/")
def home():
    all_movies = Movie.query.order_by(desc(Movie.rating)).all()
    counter = 0
    for movie in all_movies:
        counter += 1
        movie.ranking = counter
    return render_template("index.html", movies=all_movies)


@app.route('/add', methods=['GET', 'POST'])
def add():
    form = MovieForm()
    if form.validate_on_submit():
        data = tmdb_find_movie(form.title.data)
        return render_template('select.html', data=data['results'])
    return render_template('add.html', form=form)


@app.route('/add_selected/<movie_id>')
def add_selected(movie_id):
    data = tmdb_find_movie_details(movie_id)
    movie_to_add = Movie(
        title=data['title'],
        year=data['release_date'].split('-')[0],
        description=data['overview'],
        img_url='https://image.tmdb.org/t/p/w500' + data['poster_path'],
        ranking=data['vote_average'],
        rating=0,
        review=''
    )
    movies.add_movie(movie_to_add)
    return redirect(url_for('edit', movie_id=movie_to_add.id))


@app.route("/edit/<movie_id>", methods=['GET', 'POST'])
def edit(movie_id):
    if request.method == 'POST':
        print('post')
        movies.update_movie(movie_id, request.form['rating'], request.form['review'])
        return redirect(url_for('home'))
    else:
        print('get', f'id={movie_id}')
        return render_template('edit.html', movie_id=movie_id)


@app.route('/delete/<movie_id>')
def delete(movie_id):
    movies.delete_movie(movie_id)
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)
