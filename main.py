from flask import Flask, request
import requests
import re

GITHUB_TOKEN = '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'
GOOGLE_TRANSLATE_API_URL='https://translate.googleapis.com/translate_a/single?client=gtx&sl=auto&tl=en&dt=t&q=YOUR_TEXT'

app = Flask(__name__)

@app.route('/test', methods=['GET'])
def get_readme():
    url = "https://api.github.com/repos/guilhermelcosta/guilhermelcosta/readme"

    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.html+json"
    }

    response = requests.get(url, headers=headers)

    langs = re.findall(r'lang="([^"]*)"', response.text)

    # translate_text(langs[0])

    if response.status_code == 200:
        return response.text
    else:
        print(f"Erro: {response.status_code}, {response.text}")
        return None

@app.route('/translate', methods=['POST'])
def translate_text(text="teste"):

    data = request.get_json()

    response = requests.get(GOOGLE_TRANSLATE_API_URL.replace('YOUR_TEXT', data['text']))
    return response.json()[0][0]


if __name__ == '__main__':
    app.run(debug=True)
