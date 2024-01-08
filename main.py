from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/')
def index():
  return render_template("index.html")

@app.route('/submit', methods = ['GET'])
def submit():
  return {'Username': request.args.get('username'), 'Password': request.args.get('password')}

if __name__ == '__main__':
  app.run('localhost', 3000)