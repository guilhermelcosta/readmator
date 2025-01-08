from flask import Flask
from controllers.readme_controller import readme_blueprint

app = Flask(__name__)

app.register_blueprint(readme_blueprint, url_prefix="/readme")

if __name__ == '__main__':
    app.run(debug=True)
