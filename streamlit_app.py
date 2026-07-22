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

with st.form("nova_vaga"):
    titulo_vaga = st. text_input ("titulo")
    empresa_vaga = st. text_input ("empresa")
    formato_vaga = st. text_input ("formato")
    link_vaga = st. text_input ("link")
    nivel_vaga = st. text_input ("nivel")
    nova_vaga = st.form_submit_button("inserir vaga") 
if nova_vaga:  
    dados_vaga = {"titulo":titulo_vaga, "empresa":empresa_vaga,"formato":formato_vaga,"link":link_vaga,"nivel":nivel_vaga}