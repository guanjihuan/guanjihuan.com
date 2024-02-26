from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    name = 'Guan'
    return render_template('about.html', name=name)

if __name__ == '__main__':
    app.run(debug=True)