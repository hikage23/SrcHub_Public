from flask import Flask, render_template, url_for
app = Flask(__name__)
posts = [
    {
        'author' : 'Numaan Cheema',
        'title': 'TestPost1',
        'content': 'testing the usage of SrcHub',
        'date_posted': 'April 23, 2020'
    },
    {
        'title': 'TestPost2',
        'author': 'Sam Bishop',
        'content': 'testing the usage of SrcHub2',
        'date_posted': 'April 24, 2020'
    }

]

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', posts=posts)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

if __name__ == '__main__':
    app.run(debug=True)
