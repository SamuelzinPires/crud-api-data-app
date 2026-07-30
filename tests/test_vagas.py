def test_read_vagas (client):
    # Fazendo a requisição HTTP GET na rota /rota
    resposta = client.get("/vagas")
    assert resposta.status_code == 200 

def test_create_vaga(client):
    titulo_vaga = ("Vaga de Teste")
    empresa_vaga = ("empresa Teste")
    formato_vaga = ("formato Teste")
    link_vaga = ("link Teste")
    nivel_vaga = ("nivel Teste")
    test_post = client.post("/vagas",json={"titulo":titulo_vaga, "empresa":empresa_vaga,"formato":formato_vaga,"link":link_vaga,"nivel":nivel_vaga})
    assert test_post.status_code == 201
