from flask import Flask, session
from rutas_flask import main

def create_app():
    app = Flask(__name__)
    app.secret_key = 'Billed_Comet_04'
    app.register_blueprint(main)

    return app


app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)