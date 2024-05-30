import requests, json, os
from dotenv import load_dotenv
load_dotenv()

def apiCorreios(codPostagem):
    url = "https://apps3.correios.com.br/areletronico/v1/ars/ultimoevento"
    payload = json.dumps({
        "objetos": [
        str(codPostagem),
        str(codPostagem)
        ]
    })
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Basic {os.getenv("CORREIOS")}=='
    }
    return requests.request("POST", url, headers=headers, data=payload).json()  
