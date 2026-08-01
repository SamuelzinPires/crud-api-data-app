import streamlit as st  # alias padrão da lib, usado em toda chamada de interface
import requests  # lib de chamadas HTTP, usada pra falar com a API

API_URL = "http://127.0.0.1:8000/vagas"  # endereço fixo do endpoint GET /vagas

st.title("Vagas dentro da Aplicação")  # título exibido no topo da página
st.caption("visualização de vagas extraídas") # Sub Título 

st.sidebar.subheader("Filtrar")
nivel_selecionado = st.sidebar.selectbox("Selecione um nível", ["Todos", "Júnior", "Pleno", "Sênior"])  # dropdown; o valor escolhido fica guardado aqui

if "pagina" not in st.session_state:  # só roda na 1ª carga; reruns seguintes já acham a chave e pulam essa linha
    st.session_state.pagina = 0
itens_por_pagina = 10  # o "tamanho" de cada página
coluna_anterior, coluna_proxima = st.columns(2)  # 2 colunas lado a lado

with coluna_anterior:
    if st.button("Página anterior"):
        if st.session_state.pagina > 0:   # trava pra não deixar página negativa
            st.session_state.pagina -= 1

with coluna_proxima:
    if st.button("Próxima página"):
        st.session_state.pagina += 1

st.write(f"Página atual: {st.session_state.pagina + 1}")  # +1 só pra exibir "Página 1" em vez de "Página 0"
skip = st.session_state.pagina * itens_por_pagina  # página 0 pula 0, página 1 pula 10, página 2 pula 20...
if nivel_selecionado == "Todos": 
    params = {"skip": skip, "limit": itens_por_pagina}
else: 
    params = {"skip": skip, "limit": itens_por_pagina, "nivel": nivel_selecionado}
try:
    resposta = requests.get(API_URL, params=params) # busca só a página atual
    vagas = resposta.json() # pega o corpo (texto JSON) e desserializa pra lista de dicionários Python - a conversão SQL->JSON já aconteceu do lado da API; aqui é o caminho inverso (JSON->Python)
except requests.exceptions.RequestException as erro:
    st.error(f"Erro: {erro}")
    vagas = []

vagas_filtradas = vagas
 #exibição das vagas
if vagas_filtradas:  # lista vazia é "falsa" em Python - checa se sobrou algo pra mostrar
    for vaga in vagas_filtradas:                  
        st.write(f"**Título:** {vaga['titulo']}")
        st.write(f"**Empresa:** {vaga['empresa']}")
        st.write(f"**Formato:** {vaga['formato']}")
        st.write(f"**Nível:** {vaga['nivel']}")
        st.write(f"**Link:** {vaga['link']}")
        st.write("---")

#Adicionar vagas Manualmente
st.sidebar.subheader("Cadastrar nova vaga")
with st.sidebar.form("nova_vaga"):
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

 # Opção para editar a vaga - também no sidebar agora
st.sidebar.subheader("Editar / Excluir vaga")
id_vaga = st.sidebar.number_input('ID da vaga', min_value=0, step=1)   # campo compartilhado: usado tanto pelo formulário de edição (PUT) quanto pelo botão de excluir (DELETE) logo abaixo
vaga_existente = {}
try:
    resposta_get = requests.get(f"{API_URL}/{id_vaga}")
    if resposta_get.status_code == 200:
        vaga_existente = resposta_get.json()
        st.sidebar.write(f"Vaga selecionada: {vaga_existente['titulo']} - {vaga_existente['empresa']}") #oque isso aqui faz?
    else:
        st.sidebar.warning(f"Vaga com ID {id_vaga} não encontrada.")
except requests.exceptions.RequestException as erro:
    st.sidebar.error(f"Erro: {erro}")
with st.sidebar.form("editar_vaga"):
        titulo_edicao = st.text_input("titulo", value=vaga_existente.get("titulo", ""))
        empresa_edicao = st. text_input ("empresa", value=vaga_existente.get("empresa", ""))
        formato_edicao = st. text_input ("formato", value=vaga_existente.get("formato", ""))
        link_edicao = st. text_input ("link", value=vaga_existente.get("link", ""))
        nivel_edicao = st. text_input ("nivel", value=vaga_existente.get("nivel", ""))
        nova_edicao = st.form_submit_button("atualizar vaga") 
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
clik_excluir = st.sidebar.button("Excluir vaga")
if clik_excluir:
    try:
        resposta_delete = requests.delete(f"{API_URL}/{id_vaga}")
        if resposta_delete.status_code == 200:
            st.success(f"Apagado com sucesso")
        else:
            st.error(f"Erro: Status {resposta_delete.status_code}")
    except requests.exceptions.RequestException as erro:
     st.error(f"Erro: Status {erro}")
