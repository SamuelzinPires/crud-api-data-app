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

def test_update_vaga(client):
    resposta_post = client.post("/vagas", json={"titulo": "Vaga de Teste", "empresa": "empresa Teste", "formato": "formato Teste", "link": "link Teste", "nivel": "nivel Teste"})
    dados_criados = resposta_post.json()
    id_da_vaga = dados_criados["id"]
    resposta_put = client.put(f"/vagas/{id_da_vaga}", json={"titulo": "Vaga Editada", "empresa": "empresa Editada", "formato": "formato Editado", "link": "link Editado", "nivel": "nivel Editado"})
    assert resposta_put.status_code == 200

def test_delete_vaga(client):
    resposta_post = client.post("/vagas", json={"titulo": "Vaga de Teste", "empresa": "empresa Teste", "formato": "formato Teste", "link": "link Teste", "nivel": "nivel Teste"})
    dados_criados = resposta_post.json()
    id_da_vaga = dados_criados["id"]
    resposta_delete = client.delete(f"/vagas/{id_da_vaga}")
    assert resposta_delete.status_code == 200
