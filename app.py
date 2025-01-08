from flask import Flask
from controllers.github_controller import github_blueprint

app = Flask(__name__)

app.register_blueprint(github_blueprint, url_prefix="/github")

if __name__ == '__main__':
    app.run(debug=True)
