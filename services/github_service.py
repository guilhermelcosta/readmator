import base64
from datetime import datetime
from http import HTTPStatus

from services.request_service import perform_request


def create_files(current_readme_path, content, path, token):
    perform_request(f'https://api.github.com/repos/{current_readme_path}/contents/{path}', 'PUT', token, _create_body(content))


def fetch_readme(github_url, github_token):
    response = perform_request(github_url, "GET", github_token)
    if not response or response.status_code != HTTPStatus.OK:
        raise RuntimeError("Failed to fetch the README from GitHub.")
    return response.text


def _create_body(content):
    return {
        "message": f"Translation: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "content": f"{base64.b64encode(content.encode()).decode()}"
    }
