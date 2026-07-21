import csv
import requests

API_URL = "http://127.0.0.1:8000/vagas"

with open ("data/vagas_limpas.csv",  mode='r', encoding= 'utf-8') as db_vagas: #abrindo o csv para leitura.
    #ler o csv definindo colunas pelos nomes dos cabeçario com o caractere ;
    leitor_csv = csv.DictReader(db_vagas, delimiter= ';')

    for linha in leitor_csv: # Processa cada linha (vaga) do arquivo
        # Organiza os dados da linha atual com base nas suas colunas
        dados_vaga = {
            "titulo": linha["Titulo"],
            "empresa": linha["Empresa"],
            "formato": linha["Formato"],
            "link": linha["Link"],
            "nivel": linha["Nivel"]
        }
        try: # Envia os dados para a API externa via requisição POST
            resposta = requests.post(API_URL, json=dados_vaga) 
            if resposta.status_code == 201:    #Verifica se o envio deu certo (Status 201 significa Criado 
                print(f"Sucesso: Vaga '{dados_vaga['titulo']}' importada.")
            else:
                print(f"Erro ao importar '{dados_vaga['titulo']}': Status {resposta.status_code}")
        except requests.exceptions.RequestException as erro:
            print(f"Erro de conexão ao enviar vaga '{dados_vaga['titulo']}':{erro}")

        

