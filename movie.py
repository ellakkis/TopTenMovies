from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func


db = SQLAlchemy()


class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    year = db.Column(db.String(4), nullable=False)
    description = db.Column(db.String(100), nullable=False)
    rating = db.Column(db.Float)
    ranking = db.Column(db.Integer)
    review = db.Column(db.String(100), nullable=True)
    img_url = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())

    def __int__(self, title, rating, review, year, img_url, ranking):
        self.title = title
        self.rating = rating
        self.review = review
        self.year = year
        self.img_url = img_url
        self.ranking = ranking

    def __repr__(self):
        return f'<Movies {self.title}>'

    def get_movie(self, movie_id):
        return Movie.query.get_or_404(movie_id)

    def add_movie(self, movie):
        db.session.add(movie)
        db.session.commit()

    def delete_movie(self, movie_id):
        movie = Movie.query.get_or_404(movie_id)
        db.session.delete(movie)
        db.session.commit()

    def update_movie(self, movie_id, new_rating, new_review):
        book_to_edit = self.get_movie(movie_id)
        book_to_edit.rating = new_rating
        book_to_edit.review = new_review
        db.session.commit()
