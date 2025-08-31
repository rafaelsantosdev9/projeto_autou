from flask import Flask
from views import init_app

app = Flask(__name__)
app.secret_key ='analisador_de_email'

init_app(app)

# if __name__ == '__main__':
#     app.run(debug=True)