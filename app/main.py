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
    from jamef import *
    from sheets import tickets
    from correios import *
    from jadlog import *

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

