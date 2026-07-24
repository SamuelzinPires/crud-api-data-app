import streamlit as st  # alias padrão da lib, usado em toda chamada de interface
import requests  # lib de chamadas HTTP, usada pra falar com a API

API_URL = "http://127.0.0.1:8000/vagas"  # endereço fixo do endpoint GET /vagas

st.title("Vagas")  # título exibido no topo da página

nivel_selecionado = st.selectbox("Selecione um nível", ["Todos", "Júnior", "Pleno", "Sênior"])  # dropdown; o valor escolhido fica guardado aqui

resposta = requests.get(API_URL)  # chamada HTTP GET pra API - guarda a resposta inteira (status code + corpo)
vagas = resposta.json()  # pega o corpo (texto JSON) e desserializa pra lista de dicionários Python - a conversão SQL->JSON já aconteceu do lado da API; aqui é o caminho inverso (JSON->Python)

if nivel_selecionado == "Todos":  # decide qual lista vai ser usada depois
    st.write(vagas)
    vagas_filtradas = vagas  # "Todos" -> usa a lista completa, sem filtrar
else:
    vagas_filtradas = [vaga for vaga in vagas if vaga["nivel"] == nivel_selecionado]  # nível específico -> mantém só as vagas cujo campo "nivel" bate com a escolha

if vagas_filtradas:  # lista vazia é "falsa" em Python - checa se sobrou algo pra mostrar
    for vaga in vagas_filtradas:                  
        st.write(f"**Título:** {vaga['titulo']}")
        st.write(f"**Empresa:** {vaga['empresa']}")
        st.write(f"**Formato:** {vaga['formato']}")
        st.write(f"**Nível:** {vaga['nivel']}")
        st.write(f"**Link:** {vaga['link']}")
        st.write("---")
else:
    st.write("Nenhuma vaga encontrada para o nível selecionado.")

#Adicionar vagas Manualmente
with st.form("nova_vaga"):
    titulo_vaga = st. text_input ("titulo")
    empresa_vaga = st. text_input ("empresa")
    formato_vaga = st. text_input ("formato")
    link_vaga = st. text_input ("link")
    nivel_vaga = st. text_input ("nivel")
    nova_vaga = st.form_submit_button("inserir vaga") 
if nova_vaga:  
    dados_vaga = {"titulo":titulo_vaga, "empresa":empresa_vaga,"formato":formato_vaga,"link":link_vaga,"nivel":nivel_vaga} #Analisa se o valor adicionado e igual ao do schemas.py 
    try:   
        resposta_post = requests.post(API_URL,json=dados_vaga)
        if resposta_post.status_code == 201:
            st.success(f"Criado com Sucesso")
        else:
             st.error(f"Erro: Status {resposta_post.status_code}")
    except requests.exceptions.RequestException as error:
     st.error(f"Erro: Status {error}")

 # Opção para editar a vaga            
id_vaga = st.number_input('ID da vaga')          
with st.form("editar_vaga"):
        titulo_edicao = st. text_input ("titulo")
        empresa_edicao = st. text_input ("empresa")
        formato_edicao = st. text_input ("formato")
        link_edicao = st. text_input ("link")
        nivel_edicao = st. text_input ("nivel")
        nova_edicao = st.form_submit_button("inserir vaga") 
if nova_edicao:   
    dados_edicao = {"titulo":titulo_edicao, "empresa":empresa_edicao,"formato":formato_edicao,"link":link_edicao,"nivel":nivel_edicao} #Analisa se o valor adicionado e igual ao do schemas.py 
    try:
        resposta_edit = requests.put(f"{API_URL}/{id_vaga}",json=dados_edicao)
        if resposta_edit.status_code == 200:
            st.success(f"Alterado com sucesso")
        else:
             st.error(f"Erro: Status {resposta_edit.status_code}")
    except requests.exceptions.RequestException as erro:
     st.error(f"Erro: Status {erro}")

# Opção para deletar
clik_excluir = st.button("Excluir vaga")
if clik_excluir:
    try:
        resposta_delete = requests.delete(f"{API_URL}/{id_vaga}")
        if resposta_delete.status_code == 200:
            st.success(f"Apagado com sucesso")
        else:
            st.error(f"Erro: Status {resposta_delete.status_code}")
    except requests.exceptions.RequestException as erro:
     st.error(f"Erro: Status {erro}")


