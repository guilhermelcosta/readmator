import re

def extract_parameters(readme, parameter):
    return re.findall(rf'(?<={parameter}=")([^"]+)(?=")', readme)