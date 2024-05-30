import requests, json, os

cols = ['Transp. 🚚', 'NF', 'Ticket Id', 'Razão Social', 'Classe', 'Prazo de entrega', 'Status Prazo', 'Ticket Agendamento', 'Data Agendamento', 'Status Transp.', 'Atualização']
data = []
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
            'dt_agend' : str()
        }
        data.append(payload)
    else:
        break

#print(data[0])