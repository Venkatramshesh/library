from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:/Users/venka/Python100days/Starting+Files+-+library-start(1)/new-books-collections.db'
db = SQLAlchemy(app)

all_books = []
books = []


class library(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, unique=True, nullable=False)
    author = db.Column(db.String, unique=True, nullable=False)
    rating = db.Column(db.Float, unique=True, nullable=False)

@app.route('/')
def home():
    return render_template('index.html',books=all_books)


@app.route("/add", methods =['GET', 'POST'])
def add():
    if request.method == 'POST':
        #print(request.form["bookname"])
        all_books.append({"title": request.form["bookname"],"author": request.form["bookau"],"rating": request.form["rating"] })
        with app.app_context():
            db.create_all()
            post = library(title=request.form["bookname"], author=request.form["bookau"], rating=request.form["rating"])
            db.session.add(post)
            db.session.commit()
        return render_template('index.html', books=all_books)
    return render_template('add.html')

@app.route("/EditRating", methods =['GET', 'POST'])
def EditRating():
    rating = request.args.get('rating')
    if request.method == 'POST':
        for book in all_books:
            if rating == book['rating']:
                book_name = book['title']
                book['rating'] = request.form["newrating"]
                book_to_update = library.query.filter_by(title=book_name).first()
                book_to_update.rating = request.form["newrating"]
                db.session.commit()
        return render_template('index.html', books=all_books)

    return render_template('EditRating.html',books=all_books,rating=rating)

@app.route("/delete", methods =['GET', 'POST'])
def delete():
    rating = request.args.get('rating')
    print(all_books)
    for book in all_books:
        if rating == book['rating']:
            book_name = book['title']
            print(book_name)
            library.query.filter_by(title=book_name).delete()
            db.session.commit()
            all_books.remove(book)
            break

    return render_template('index.html', books=all_books)

# with app.app_context():
#     post = Bookmodel(title=book['title'], author=book['author'], rating=book['rating'])
#     db.session.add(post)


if __name__ == "__main__":
    app.run(debug=True)






