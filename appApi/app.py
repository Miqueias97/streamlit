from flask import Flask
import requests, json, datetime, time, os
from jamef import tokenJamef
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)


@app.route('/atualiza-envios-chama-nas-mil')
def index():
    inicio = time.time() 
    data_inf = []
    for i in requests.get(f'https://script.google.com/macros/s/AKfycbyKPUmiuTnTbGid3to46v_2bCEitpMnzXdPCxaFGq2QEbZmvmoGP8sVzwTJyV4zlSo1mQ/exec').json()['status']:
        if i[0] != '' and i[0] != 'Ticket status':
            payload = {
                "transp" : i[4],
                'nf' : i[2],
                'ticket_id' : i[5],
                'nome' : i[9],
                'clase' : i[7],
                'prazo' : str(i[3]),
                'status_prazo' : i[15],
                'tk_agend' : i[13],
                'dt_agend' : str(i[14]),
                'cod_post' : str(i[12])
            }
            data_inf.append(payload)
        elif i[0] == '':
            break
    
    tk_jamef = tokenJamef()
    response_apis = []
    with requests.Session() as session:
        for i in data_inf:
            status = 'erro'
            data = datetime.datetime.today().date()
            if i['transp'] == 'Jadlog':
                url = "https://prd-traffic.jadlogtech.com.br/embarcador/api/tracking/consultar"
                payload = json.dumps({
                "consulta": [
                    {
                    "df": {
                        "nf": str(i['nf']),
                        "cnpjRemetente": "17668689000120",
                        "tpDocumento": 1
                    }
                    }
                ]
                })

                headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {os.getenv("JAD")}'
                }
                response = session.post(url, headers=headers, data=payload).json()
                try:
                    status = response['consulta'][0]['erro']['descricao']
                except:
                    status = response['consulta'][0]['tracking']['eventos']
                    data = status[len(status) - 1 ]['data']
                    status = status[len(status) - 1 ]['status']

            elif i['transp'] == 'Correios':
                url = "https://apps3.correios.com.br/areletronico/v1/ars/ultimoevento"
                payload = json.dumps({
                    "objetos": [
                    str(i['cod_post']),
                    str(i['cod_post'])
                    ]
                })
                headers = {
                    'Content-Type': 'application/json',
                    'Authorization': f'Basic {os.getenv("CORREIOS")}=='
                }
                response = session.post(url, headers=headers, data=payload).json()
                try:
                    status = response[0]['eventos'][0]['descricaoEvento']
                    data = response[0]['eventos'][0]['dataEvento']
                except:
                    status = response[0]['mensagem']

            elif i['transp'] == 'Jamef':
                url = "https://api.jamef.com.br/rastreamento/ver"
                payload = json.dumps({
                    'documentoResponsavelPagamento' : '17668689000120',
                    'numeroNotaFiscal' : str(i['nf'])
                })
                headers = {
                'Accept': 'application/json',
                'Authorization': 'Bearer ' + tk_jamef,
                'Cookie': 'Path=/; Path=/'
                }

                response = session.post(url, headers=headers, data=payload).json()
                try:
                    status = str(response['message']['message']).split(',')[0]
                except:
                    status = response['conhecimentos'][0]['historico'][0]['statusRastreamento']
                    data = response['conhecimentos'][0]['historico'][0]['dataAtualizacao']
            else:
                pass
    
            info = i
            info['status'], info['dt_att'] = status, data
            response_apis.append(info)

    #response_apis = json.dumps(response_apis)
    return response_apis



if __name__ == '__main__':
    app.run(debug=False)