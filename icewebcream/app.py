from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return "<h1>O IceWebCream está funcionando perfeitamente no VS Code!</h1>"

if __name__ == '__main__':
    app.run(debug=True)