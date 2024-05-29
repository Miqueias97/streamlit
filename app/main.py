import streamlit as st
import streamlit_authenticator as stauth
import pandas as pd
import requests, json, os
import yaml
from yaml.loader import SafeLoader
st.set_page_config(layout="wide")

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
    def cria_lista():
        import time, datetime
        def tickets():
            data = []
            cont = 0
            for i in requests.get('https://script.google.com/macros/s/AKfycbyKPUmiuTnTbGid3to46v_2bCEitpMnzXdPCxaFGq2QEbZmvmoGP8sVzwTJyV4zlSo1mQ/exec').json()['status']:
                if cont > 0 and i[0] != '':
                    data.append(i)
                cont +=1
            return data

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
        try:
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
                    prazo = str(i[3]).split('T')
                    prazo = datetime.datetime.strptime(prazo[0], '%Y-%m-%d')
                    prazo = prazo.strftime('%d/%m/%Y')
                    instalacao, dt_inst = '', ''
                    if len(str(i[13]).strip()) != 0 and str(i[13]) != 'None':
                        instalacao = f'<a href="https://app.hubspot.com/contacts/5282301/record/0-5/{i[13]}">{i[13]}<a/>'
                        dt_inst = str(i[3]).split('T')
                        dt_inst = datetime.datetime.strptime(dt_inst[0], '%Y-%m-%d')
                        dt_inst = datetime.datetime.strptime(prazo[0], '%Y-%m-%d')
                        dt_inst = dt_inst.strftime('%d/%m/%Y')
                    a = [i[4], i[2], f'<a href="https://app.hubspot.com/contacts/5282301/record/0-5/{i[5]}">{i[5]}<a/>', i[9], i[7], prazo, i[15], instalacao, dt_inst]
                    a.extend([status, data])
                    dados.append(a)
        except:
            time.sleep(10)  
                
        return dados           

    dados = cria_lista()
    cols = ['Transp. 🚚', 'NF', 'Ticket Id', 'Ticket Name', 'Classe', 'Prazo de entrega', 'Status Prazo', 'Ticket Agendamento', 'Data Agendamento', 'Status Transp.', 'Atualização']
    df = pd.DataFrame.from_records(dados, columns=cols)
    qtd_tk = len(dados)
    st.markdown("# Acompanhamento Envios 🚚")
    atrasados = df[df['Status Prazo'] == 'Atrasado']
    st.html(f'''
        <table style="text-align: center;
                border: .01rem;
                border-radius: .5rem;
                padding: 0%;
                background-color: #07074e; 
                width: 20rem; 
                height : 3rem;
                ">
            <thead>
            <tr>
                <th style="color: white;">Qtd Tickets</th>
                <th style="color: white;">Qtd Em Atraso</th>
            </tr>
            </thead>
            <tbody>
            <tr>
                <td style="background-color: white; 
                border : solid .01rem;
            border-radius: .5rem;
            ">{qtd_tk}</td>
                <td style="background-color: white; 
                border : solid .01rem;
            border-radius: .5rem;
            ">{len(atrasados)}</td>
            </tr>
            </tbody>
        </table>
      ''')

    if True:# st.checkbox('Listar Tickets'):
        df = df.sort_values('Prazo de entrega')
        df = df.values.tolist()
        a = '''
                <table style="text-align: center;
                        border: .01rem;
                        border-radius: .5rem;
                        padding: 0%;
                        background-color: #07074e; >
                    <thead>
                    <tr>
                    <th style="color: white;"></th>
            '''
        for i in cols:
            a+=  f'<th style="color: white;">{i}</th>'

        a+=   '''
            </tr>
            </thead>
            <tbody>'''
        
        for i in df:
            a += '<tr>'
            for j in i:
                a += f'''<td style="background-color: white; 
                    border : solid .01rem;
                ">{j}</td>
                    '''
            
            a+= '</tr>'

        a += '''
            </tbody>
            </table>   
      '''
        #df = df.to_html(escape=False, index=None)
        st.write(a, unsafe_allow_html=True)

    

elif st.session_state["authentication_status"] is False:
    st.error('Usuário/Senha is inválido')

