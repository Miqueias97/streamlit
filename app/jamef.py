import requests
import json, os
from dotenv import load_dotenv
load_dotenv()

def tokenJamef():
    urltk = "https://api.jamef.com.br/login"
    payload = json.dumps({
        'username' : 'conciergepio',
        'password' : os.getenv('JAMEF')
    })
    headers = {
    'Accept': 'application/json',
    'Content-Type': 'text/plain',
    'Cookie': 'Path=/'
    }
    response = requests.request("POST", urltk, headers=headers, data=payload)
    response = response.json()

    return response['access_token']




def apiJamef(nf, token):
    url = "https://api.jamef.com.br/rastreamento/ver"
    payload = "{\r\n    \"documentoResponsavelPagamento\" : \"17668689000120\",\r\n    \"numeroNotaFiscal\": \" " +str(nf) +"\"\r\n}"
    headers = {
    'Accept': 'application/json',
    'Authorization': 'Bearer ' + token,
    'Cookie': 'Path=/; Path=/'
    }

    return requests.request("POST", url, headers=headers, data=payload).json()