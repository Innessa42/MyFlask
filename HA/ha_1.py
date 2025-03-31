from flask import Flask
app = Flask(__name__)  # Создаем объект Flask
@app.route('/')
def get_hello():
    return 'Hello Flask!'
@app.route('/user/', defaults={"name": "alice"})

@app.route('/user/<name>')
def get_name(name):
    return f'Hello {name}'



if __name__ == '__main__':
    app.run(debug=True)




