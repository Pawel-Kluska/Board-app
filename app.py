from flask import Flask, render_template, url_for

app = Flask(__name__)

title_home = 'Home'

@app.route('/')
@app.route('/home')
def home():  # put application's code here
    return render_template('home.html', title=title_home)


@app.route('/about')
def about():
    return render_template('about.html')


if __name__ == '__main__':
    app.run()
