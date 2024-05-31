import streamlit as st
import streamlit_authenticator as stauth
import pandas as pd
import requests, json
st.set_page_config(layout="wide")

headers = {
  'apikey': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImxncXBjY2J0b2FmanlhZ2NhdmJkIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MTI3NTkxNzYsImV4cCI6MjAyODMzNTE3Nn0.8Eztx6ygiqK6jP48BC7TsXwevH0Ji-GbpRdMkOI-_m0'
}

response = requests.request("GET", 'https://lgqpccbtoafjyagcavbd.supabase.co/rest/v1/users', headers=headers).json()

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
    st.markdown("# Acompanhamento Envios 🚚")
    

    dados = requests.get('https://appapi.fly.dev/').json()
    df = pd.DataFrame.from_dict(dados)
    
    dados = []
    for i in df.values.tolist():
        if len(str(i[10]).strip()) > 0:
            tk_agd = f'<a href="https://app.hubspot.com/contacts/5282301/record/0-5/{i[10]}" style="text-decoration: none;">🔗 {i[10]}</a>'            
            dt_agen = str(i[2]).split('T')[0]
            dt_agen = str(dt_agen).split('-')
            dt_agen = f'{dt_agen[2]}/{dt_agen[1]}/{dt_agen[0]}'
        else:
            tk_agd, dt_agen = '', ''
        dt = str(i[6]).split('T')[0]
        dt = str(dt).split('-')
        dt = f'{dt[2]}/{dt[1]}/{dt[0]}'
        
        item = [f'<a href="https://app.hubspot.com/contacts/5282301/record/0-5/{i[9]}" style="text-decoration: none;">🔗 Link</a>' , i[11], i[4], i[9], i[5], i[0], dt, i[8], tk_agd, dt_agen, i[7]]
        dados.append(item)
    
    cols = ['link', 'Transp. 🚚', 'NF', 'Ticket Id', 'Razão Social', 'Classe', 'Prazo de entrega', 'Status Prazo', 'Ticket Agendamento', 'Data Agendamento', 'Status Transp.']
    
    df = pd.DataFrame.from_records(dados, columns=cols)
    

    
    df = df.sort_values('Prazo de entrega')
    
    # filtros
    tickets = [' ']
    tickets.extend(df['Ticket Id'].unique().tolist())
    option = st.sidebar.selectbox( "*Pesquisar Ticket ID 🔍*", tickets)

    cliente = [' ']
    cliente.extend(df['Razão Social'].unique().tolist())
    filter_cliente = st.sidebar.selectbox( "*Pesquisar por Cliente 🔍*", cliente)

    filter_agendado = st.sidebar.selectbox('Ticket possui agendamento?', (' ', 'Sim', 'Não'))

    classe = df['Classe'].unique().tolist()
    filtra_classe = st.sidebar.multiselect('Classe do pedido',
                                  classe)
    
    
    status = df['Status Prazo'].unique().tolist()
    status_filter = st.sidebar.multiselect('Status do Envio',
                                  status)
    
    transport = df['Transp. 🚚'].unique().tolist()
    filter_transp = st.sidebar.multiselect('Transportadora',
                                  transport)
    
    status_transp = df['Status Transp.'].unique().tolist()
    status_transp_filter = st.sidebar.multiselect('Status Informado pela Transportadora',
                                  status_transp)
    
    if len(filtra_classe) == 0:
        filtra_classe = classe
    if len(status_filter) == 0:
        status_filter = status
    if len(filter_transp) == 0:
        filter_transp = transport
    if len(status_transp_filter) == 0:
        status_transp_filter = status_transp
    
    filtros = (df['Status Prazo'].isin(status_filter)) & (df['Classe'].isin(filtra_classe)) & (df['Transp. 🚚'].isin(filter_transp)) & \
              (df['Status Transp.'].isin(status_transp_filter))
    
    df = df[filtros]

    if option != None and len(str(option).strip()) > 0:
        filtros = (df['Ticket Id'] == option)
        df = df[filtros]

    if filter_cliente != None and len(str(filter_cliente).strip()) > 0:
        filtros = (df['Razão Social'] == filter_cliente)
        df = df[filtros]

    if len(str(filter_agendado).strip()) > 0:
        if filter_agendado == 'Sim':
            filtros = (df['Ticket Agendamento'] != "")
            df = df.sort_values('Data Agendamento')
        else:
            filtros = (df['Ticket Agendamento'] == "")
        df = df[filtros]

    

    qtd_tk, atrasados = len(df), df[df['Status Prazo'] == 'Atrasado']
    # controi tabela informando qtd total e em atraso
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

