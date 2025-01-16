from services.request_service import perform_request



def create_files(path, token):
    perform_request(f'https://api.github.com/repos/guilhermelcosta/guilhermelcosta/contents/{path}', 'POST', token)
