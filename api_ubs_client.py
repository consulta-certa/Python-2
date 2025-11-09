import requests

def buscar_ubs_por_cep():
    """Consulta a API pública de UBS hospedada no Render."""
    cep = input("Digite o CEP (apenas números): ").strip()
    if not cep.isdigit() or len(cep) != 8:
        print("❌ CEP inválido. Deve conter exatamente 8 números.")
        return
    
    url = f"https://buscar-ubs-perto-api.onrender.com/ubs/perto?cep={cep}"
    print(f"\n🔎 Consultando UBS para o CEP {cep}...")
    
    try:
        response = requests.get(url, timeout=120)
        response.raise_for_status()
        dados = response.json()

        if "erro" in dados:
            print(f"❌ {dados['erro']}")
            return
        
        print(f"\n🏙️ {dados['cidade']} - {dados['uf']}")
        print("🏥 UBS próximas:")
        for ubs in dados["ubs_proximas"]:
            print(f"  - {ubs['nome']}")
            print(f"    📍 {ubs['endereco']}")
            if ubs["distancia_km"]:
                print(f"    📏 Distância: {ubs['distancia_km']} km")
            print("-" * 50)
    except Exception as e:
        print(f"⚠️ Erro ao consultar a API: {e}")
