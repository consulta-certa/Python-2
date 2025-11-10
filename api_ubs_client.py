import requests

def consultar_api_ubs(cep):
    """
    Consulta a API de UBS para um CEP específico e retorna os dados.
    """
    url = f"https://buscar-ubs-perto-api.onrender.com/ubs/perto?cep={cep}"
    print(f"Consultando o serviço para o CEP {cep}...")
    
    try:
        response = requests.get(url, timeout=120)
        response.raise_for_status()  # Lança uma exceção para respostas com erro (4xx ou 5xx).
        return response.json()
    except requests.exceptions.Timeout:
        print("Erro: A requisição excedeu o tempo limite.")
        return None
    except requests.exceptions.RequestException as e:
        print(f"Erro de conexão ao consultar a API: {e}")
        return None

def formatar_e_exibir_resultados(dados):
    """
    Formata e exibe os dados das UBS recebidos da API.
    """
    if not dados:
        print("Não foi possível obter uma resposta da API.")
        return

    if "erro" in dados:
        print(f"Aviso: {dados['erro']}")
        return

    print(f"\nResultados para a cidade de {dados.get('cidade', 'N/A')} - {dados.get('uf', 'N/A')}")
    
    ubs_proximas = dados.get("ubs_proximas")
    if not ubs_proximas:
        print("Nenhuma UBS foi encontrada nas proximidades para o CEP informado.")
        return

    print("UBS próximas encontradas:")
    for ubs in ubs_proximas:
        print("-" * 40)
        print(f"  Nome: {ubs.get('nome', 'Não informado')}")
        print(f"  Endereço: {ubs.get('endereco', 'Não informado')}")
        distancia = ubs.get('distancia_km')
        if distancia is not None:
            print(f"  Distância: {distancia} km")

def main_api_ubs_client():
    """
    Orquestra a busca de UBS: pede o CEP ao usuário, consulta a API e exibe os resultados.
    """
    cep = input("Digite o CEP para a busca (apenas números): ").strip()
    if not cep.isdigit() or len(cep) != 8:
        print("Formato de CEP inválido. Deve conter exatamente 8 dígitos numéricos.")
        return
    
    dados_ubs = consultar_api_ubs(cep)
    formatar_e_exibir_resultados(dados_ubs)

if __name__ == "__main__":
    main_api_ubs_client()