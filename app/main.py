import streamlit as st
import streamlit_authenticator as stauth
import pandas as pd
import requests, json, os
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
    
    dados = '' #cria_lista()
    cols = ['Transp. 🚚', 'NF', 'Ticket Id', 'Razão Social', 'Classe', 'Prazo de entrega', 'Status Prazo', 'Ticket Agendamento', 'Data Agendamento', 'Status Transp.', 'Atualização']
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

    df = df.sort_values('Prazo de entrega')
    # filtros
    
    status = df['Classe'].unique().tolist()
    filtra_classe = st.sidebar.multiselect('Classe do pedido',
                                  status,
                                  default=status)

    status = df['Status Prazo'].unique().tolist()
    status_filter = st.sidebar.multiselect('Status do Envio',
                                  status,
                                  default=status)
    
    transport = df['Transp. 🚚'].unique().tolist()
    filter_transp = st.sidebar.multiselect('Transportador',
                                  transport,
                                  default=transport)
    
    filtros = (df['Status Prazo'].isin(status_filter)) & (df['Classe'].isin(filtra_classe)) & (df['Transp. 🚚'].isin(filter_transp))
    
    df = df[filtros]
    
    
    data = df.values.tolist()
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
    
    for i in data:
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
    st.write(a, unsafe_allow_html=True)

    

elif st.session_state["authentication_status"] is False:
    st.error('Usuário/Senha is inválido')

