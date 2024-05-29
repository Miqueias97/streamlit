import streamlit as st
import streamlit_authenticator as stauth
import pandas as pd
import requests, json, os
import yaml
from yaml.loader import SafeLoader

background_image = """
<style>
[data-testid="stAppViewContainer"] > .main {
    background-color: #07074E;
    margin : 0px;
    padding: 0%;
    width: 100%
}
</style>
"""
#st.markdown(background_image, unsafe_allow_html=True)


payload = ""
headers = {
  'apikey': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImxncXBjY2J0b2FmanlhZ2NhdmJkIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MTI3NTkxNzYsImV4cCI6MjAyODMzNTE3Nn0.8Eztx6ygiqK6jP48BC7TsXwevH0Ji-GbpRdMkOI-_m0'
}

response = requests.request("GET", 'https://lgqpccbtoafjyagcavbd.supabase.co/rest/v1/users', headers=headers, data=payload).json()

config = {
    'credentials': {
        'usernames': {
        }
    }, 
    'cookie': {
        'expiry_days': 1, 
        'key': 'some_signature_key', 
        'name': 'some_cookie_name'
    }
}

for i in response:
    config['credentials']['usernames'][i['user']] = {
        'name' : str(i['nome']),
        'logged_in': False,
        'password': str(i['pass'])
    }




authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)

authenticator.login()

if st.session_state["authentication_status"]:
    authenticator.logout()
    st.write(f'Bem Vindo *{st.session_state["name"]}*')
    from correios import *
    from jadlog import *
    def tickets():
        import gspread as gs
        import json, os
        urlBase = 'https://docs.google.com/spreadsheets/d/'
        idBaseEnvios = "1BCUxW2yuXlY3iMzvlXO9HPfle78uLiedCUlHBYXBfKA/edit#gid=0"

        gc = gs.service_account_from_dict({
        "type": "service_account",
        "project_id": "integracao-389616",
        "private_key_id": '25fb100c458cd8cdaa09d86debfc4126469f1404',
        "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQCt+K88L059fRdK\n4qx/ELGiV8rxlUICfvAmAGOsPj38hIPIVENuES+yh9z6fNo0AOPA1xOA1iBUn0F0\nGv8Fh3ttVEeR2bS3ACU/S9UsKqNPjGHz55eBF3qBA4s5zmg/0WXVPXcXoz3ZiJSh\nO1wZSq7lPPp3+OFQJnlrSxDOm+LOXL/7Mf01npkrLAOlE4WSh1/P0W0YvrilDm0Q\nFTKuf4b8TOEE6wRD496ScABWsUyPUUiUjFo7pzbfs8oEXV3Jl0l6XsXzrrcJaV/2\nfNzLEP9nhUbBt3zRd9NOWUMLbmRuupSQ6Kn1odUkNkjVEKQa4iq/pep5dFqD/ufm\nVZ09B5ndAgMBAAECggEAGBe8jOUwRYixVRmXMfGp6AWogVReU+Iod9rN8uibxQDF\nD1U8EV4n8N2H6Nipj1IgOHCQruL4jz+O3PlwH9/nY/isALLZqA5JGj7yQq+U9ktG\ntXR5MtOBj6Rh/5tqLIxfQezFNWzR//I+QyXpV0dUeUK8nSjGa0cowYcfyL0l59YN\n3fVtLSoA0O98/RtPbFwhuqSr6tZWCbhHXzcCVEZ5vRPKZZjSKn8YV4mfrcHTTwfN\nnT0gZf1VaonNH13Q57ptsF/sNSGZjug43/yAo6gbPhLf3q8CpyyHzk1npITHxdfk\n8zQ7Y1YKvCdX8DMd3Oc+60KxHbKT2Sa0khxSm+GrsQKBgQDg8Naw6uW04FwDCHEe\nWT0TqA9BlsV6HHVcnWT3fNmCa0cmJSziUGm1lQ1Gg+kOqzTa6l15PBVn9J4goCEV\nhKdhGqNRzGA2aslYtXxvyu/gHi+thZU/SFKlSYjzRKOlI5HtimrG3V6oIHgx0hwM\nAIMW1HAbCUJdhSX65cqNDH8tewKBgQDF/jEDVXa4buhuX7NP4NkTNpVrRIiB43gz\njQW1hDa3Ll7Dhbr67tDXrncrV8Ku6ufVbzYNs7PJDhUbbLov9+V84q04qj7bURBo\ngNJgIktZjjXz5vuA8YgLE3Ji5wxKVTWpTqqbAwLOoYawsS8XmEC7nnGY0ekPR+LO\nSmsdC756hwKBgQCLVUN3NRlyb+Mu0cTX6qkFiv1gQFc0a3pbEveewYwt1+urei2S\nRgMkwh4GBuGO/4fu7mtWFFyiFwj35ph3rsLLSGfP3EvgiUcNFuXsjYUGi0w3LN6k\n41SmI6WcInFHcoAK5sl7Q1ZFyE8LdT2ARbTtqEuEw7iDG13KSxqrQglpDwKBgE8A\nXEI+Sb7R0kCoQv4uc69s6jYBBI7/WqkHLi39cW+qOvm9VJxnykElRjuvKulspdDO\nLT1OZQBmdBmbSrd1LMamFAQ2Ohp8wBVSwZ7GUFaNng2SLuyGc4gn3E6GbqsCUQUb\ndIuhqe8VGI9MQ8QgZkP2ttEJgPst7dvuacsPMpPlAoGBAJOYzRWwGjULv2hKbzg4\ngF4DE8daKG6VF/Q3J6YTYKoqaNUaNh89MNQMY7/tqse0x+RiQzXVVVGnBeHjCe9D\nv/cZJTFP9AsGW+7yEYz6gTSYMhmNouQ5zd2GbxTwSh5i1KR0P417oVg2qk6M//nt\nCM8PbAq5Bu2ZX2c/ihzvodOj\n-----END PRIVATE KEY-----\n",
        "client_email": "teste-sheets@integracao-389616.iam.gserviceaccount.com",
        "client_id": "115043052029499719431",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/teste-sheets%40integracao-389616.iam.gserviceaccount.com",
        "universe_domain": "googleapis.com"
        })
        return gc.open_by_url(urlBase + idBaseEnvios).worksheet('tickets').get_values('A2:Z1000')

    def tokenJamef():
        urltk = "https://api.jamef.com.br/login"
        payload = json.dumps({
            'username' : 'conciergepio',
            'password' : 'pio@1766'
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
        'Authorization': f'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJqdGkiOjk4MDI1LCJkdCI6IjIwMjIwNDE4In0._rU3LuAjO3BtEmAGpZapvkugsO8jCc55Du2eWBwmuOg',
        'Cookie': 'API-Traffic=ec5e46417cd40c694f9768dc01c3a402|101a1723e438203b25c1377d32e8b622'
        }

        return requests.request("POST", url, headers=headers, data=payload).json()    

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
            'Authorization': f'Basic MTgwNTc2MjQ6TkdmZDdvM0dwUkp0enNhd0VHc1EwVzRBQXNZcXNDMTBIalhtVmxpdw=='
        }
        return requests.request("POST", url, headers=headers, data=payload).json()    

    tkJamef = tokenJamef()
    dados = []
    for i in tickets():
            data = ''
            status = ''
            if i[4] == 'Jadlog':
                info = jadlog(i[2])
                try:
                    status = info['consulta'][0]['erro']['descricao']
                except:
                    status = info['consulta'][0]['tracking']['eventos']
                    data = status[len(status) - 1 ]['data']
                    status = status[len(status) - 1 ]['status']

            if i[4] == 'Jamef':
                info = apiJamef(i[2], tkJamef)
                try:
                    status = str(info['message']['message']).split(',')[0]
                except:
                    status = info['conhecimentos'][0]['historico'][0]['statusRastreamento']
                    data = info['conhecimentos'][0]['historico'][0]['dataAtualizacao']

            try:
                if i[4] == 'Correios':
                    cod = str(i[12]).replace(" ", '')
                    info = apiCorreios(cod)
                    try:
                        status = info[0]['eventos'][0]['descricaoEvento']
                        data = info[0]['eventos'][0]['dataEvento']
                    except:
                        status = info[0]['mensagem']
            except:
                status = 'Erro'
            a = [i[4], i[2], f'<a href="https://app.hubspot.com/contacts/5282301/record/0-5/{i[5]}">{i[5]}<a/>', i[9], i[7], i[3], i[15], i[13], i[14]]
            a.extend([status, data])
            dados.append(a)
            

    cols = ['🚚', 'NF', 'Ticket Id', 'Ticket Name', 'Classe', 'Prazo de entrega', 'Status Prazo', 'Ticket Agendamento', 'Data Agendamento', 'Status Transp.', 'Atualização']
    df = pd.DataFrame.from_records(dados, columns=cols)
    df = df.sort_values('Prazo de entrega')
    df = df.to_html(escape=False, index=None)
    st.write(df, unsafe_allow_html=True)
    

elif st.session_state["authentication_status"] is False:
    st.error('Usuário/Senha is inválido')

