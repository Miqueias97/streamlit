import requests, json, os
from dotenv import load_dotenv
load_dotenv()

def jadlog(nf):
    url = "https://prd-traffic.jadlogtech.com.br/embarcador/api/tracking/consultar?nf=54004"

    payload = json.dumps({
    "consulta": [
        {
        "df": {
            "nf": str(nf),
            "cnpjRemetente": "17668689000120",
            "tpDocumento": 1
        }
        }
    ]
    })

    headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {os.getenv("JAD")}',
    'Cookie': 'API-Traffic=ec5e46417cd40c694f9768dc01c3a402|101a1723e438203b25c1377d32e8b622'
    }

    return requests.request("POST", url, headers=headers, data=payload).json()