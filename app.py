from flask import Flask
from controllers.github_controller import github_blueprint
# from controllers.translate_controller import translate_blueprint

app = Flask(__name__)

# Registrar Blueprints (rotas separadas em diferentes módulos)
app.register_blueprint(github_blueprint, url_prefix="/github")
# app.register_blueprint(translate_blueprint, url_prefix="/translate")

if __name__ == '__main__':
    app.run(debug=True)
