from datetime import datetime
from flask import Flask, render_template, redirect, url_for, request
import psycopg2
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from sqlalchemy import ForeignKey
from sqlalchemy.orm import backref, relationship
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:1234@localhost:5432/test"
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////mnt/c/Users/antho/Documents/blog/blog.db'
app.config['SECRET_KEY'] = 'Thisissupposedtobesecret!'
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)


class Blogpost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    subtitle = db.Column(db.String(50))
    author = db.Column(db.String(20))
    date_posted = db.Column(db.DateTime)
    content = db.Column(db.Text)


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


# IMPLEMENTED (Fills in p_user table in db)
class P_user(UserMixin, db.Model):
    __tablename__ = 'p_user'
    user_ID = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))
    phone_no = db.Column(db.String(80))

    # Traceback error when implementing the below relation. Not sure why?
    # followers = db.relationship('Followers', backref='p_user', cascade='all, delete-orphan', lazy='dynamic')

    def get_id(self):
        return self.user_ID

#NOT IMPLEMENTED YET
class Article(UserMixin, db.Model):
    __tablename__ = 'article'
    ar_category = db.Column(db.String(205), unique=True)
    ar_datecreated = db.Column(db.String(215), unique=True)
    ar_authorname = db.Column(db.String(215), unique=True)
    ar_description = db.Column(db.String(215), unique=True)
    ar_title = db.Column(db.String(215), unique=True)
    ar_indexno = db.Column(db.Integer, primary_key=True)

#NOT IMPLEMENTED YET
class Photo(UserMixin, db.Model):
    __tablename__ = 'photo'
    pho_category = db.Column(db.String(215), unique=True)
    pho_datecreated = db.Column(db.String(215), unique=True)
    pho_authorname = db.Column(db.String(215), unique=True)
    pho_description = db.Column(db.String(215), unique=True)
    pho_title = db.Column(db.String(215), unique=True)
    pho_indexno = db.Column(db.Integer, primary_key=True)

#NOT IMPLEMENTED YET
class Contributor(UserMixin, db.Model):
    __tablename__ = 'contributor'
    num_of_contributor = db.Column(db.Integer, primary_key=True)

#NOT IMPLEMENTED YET
class Followers(UserMixin, db.Model):
    __tablename__ = 'followers'
    # id=db.Column(db.Integer, db.ForeignKey('p_user.user_ID'),nullable=False)
    numof_followers = db.Column(db.Integer, primary_key=True)
    #ID = db.Column(db.Integer, db.ForeignKey('p_user.user_ID '), nullable=False)

#NOT IMPLEMENTED YET
class Comment(UserMixin, db.Model):
    com_length = db.Column(db.String(215), unique=True)
    com_date = db.Column(db.String(215), unique=True)
    com_visibility = db.Column(db.String(215), unique=True)
    com_index = db.Column(db.Integer, primary_key=True)
# login route
@login_manager.user_loader
def load_user(user_ID):
    return P_user.query.get(int(user_ID))


# LoginForm
class LoginForm(FlaskForm):
    user_name = StringField('user_name', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('remember me')


# RegisterForm
class RegisterForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    user_name = StringField('user_name', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
    phone = StringField('phone', validators=[InputRequired(), Length(min=8, max=80)])


@app.route('/')
def index1():
    return render_template('index1.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = P_user.query.filter_by(user_name=form.user_name.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                return redirect(url_for('index'))

        return '<h1>Invalid username or password</h1>'
        # return '<h1>' + form.username.data + ' ' + form.password.data + '</h1>'

    return render_template('login.html', form=form)


# Registration form route
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        new_user = P_user(user_name=form.user_name.data, email=form.email.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('index1'))

        # return '<h1>' + form.username.data + ' ' + form.email.data + ' ' + form.password.data + '</h1>'

    return render_template('signup.html', form=form)


# Dashboard after user logs in
@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', name=current_user.user_name)


# logout route after someone has logged out
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index1'))


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/post/<int:post_id>')
def post(post_id):
    post = Blogpost.query.filter_by(id=post_id).one()

    return render_template('post.html', post=post)


@app.route('/add')
def add():
    return render_template('add.html')


@app.route('/addpost', methods=['POST'])
def addpost():
    title = request.form['title']
    subtitle = request.form['subtitle']
    author = request.form['author']
    content = request.form['content']

    post = Blogpost(title=title, subtitle=subtitle, author=author, content=content, date_posted=datetime.now())

    db.session.add(post)
    db.session.commit()

    return redirect(url_for('index1'))

@app.route('/index')
def index():
    posts = Blogpost.query.order_by(Blogpost.date_posted.desc()).all()
    return render_template('index.html', posts=posts)


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
