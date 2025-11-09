from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import pandas as pd
import os
import json
from math import radians, sin, cos, sqrt, atan2

app = Flask(__name__)
CORS(app)
CSV_PATH = "Unidades_Basicas_Saude-UBS.csv"

# 🔹 Função de cálculo de distância (Haversine)
def calcular_distancia(lat1, lon1, lat2, lon2):
    """Calcula a distância entre dois pontos (em km)"""
    R = 6371  # Raio médio da Terra em km
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c

# 🔹 Rota principal
@app.route("/ubs/perto", methods=["GET"])
def buscar_ubs():
    """Busca UBS mais próximas com base no CEP informado"""

    # 🧠 Validação e limpeza do CEP
    cep = request.args.get("cep", "").strip()
    cep = "".join(filter(str.isdigit, cep))  # mantém apenas números

    if not cep or len(cep) != 8:
        return jsonify({"erro": "CEP inválido. Use apenas números com 8 dígitos."}), 400

    print(f"\n🔍 Buscando UBS para o CEP: {cep}")

    # 1️⃣ Consultar CEP via ViaCEP
    via_cep_url = f"https://viacep.com.br/ws/{cep}/json/"
    try:
        resposta = requests.get(via_cep_url, timeout=10)
        resposta.raise_for_status()
        dados_cep = resposta.json()
    except Exception as e:
        return jsonify({"erro": f"Erro ao consultar ViaCEP: {e}"}), 500

    cidade = dados_cep.get("localidade")
    uf = dados_cep.get("uf")
    ibge_codigo = dados_cep.get("ibge")

    if not cidade or not uf or not ibge_codigo:
        return jsonify({"erro": "CEP inválido ou sem código IBGE"}), 400

    # 2️⃣ Obter coordenadas aproximadas do CEP
    lat_usuario = lon_usuario = None
    try:
        nominatim_url = f"https://nominatim.openstreetmap.org/search?postalcode={cep}&country=Brazil&format=json"
        resp_coord = requests.get(nominatim_url, headers={"User-Agent": "consulta-certa-app"}, timeout=10)
        if resp_coord.status_code == 200 and resp_coord.json():
            localizacao = resp_coord.json()[0]
            lat_usuario = float(localizacao["lat"])
            lon_usuario = float(localizacao["lon"])
            print(f"📍 Localização aproximada: {lat_usuario}, {lon_usuario}")
        else:
            print("⚠️ Não foi possível obter coordenadas do CEP.")
    except Exception as e:
        print(f"⚠️ Erro ao buscar coordenadas: {e}")

    # 3️⃣ Ler o CSV local de UBS
    if not os.path.exists(CSV_PATH):
        return jsonify({"erro": f"Arquivo {CSV_PATH} não encontrado"}), 500

    try:
        df = pd.read_csv(CSV_PATH, sep=";", dtype=str, on_bad_lines="skip")
        df["LATITUDE"] = pd.to_numeric(df["LATITUDE"].str.replace(",", ".", regex=False), errors="coerce")
        df["LONGITUDE"] = pd.to_numeric(df["LONGITUDE"].str.replace(",", ".", regex=False), errors="coerce")
        df = df.dropna(subset=["LATITUDE", "LONGITUDE"])
    except Exception as e:
        return jsonify({"erro": f"Erro ao processar CSV: {e}"}), 500

    # 4️⃣ Filtrar por cidade/IBGE
    df["IBGE"] = df["IBGE"].astype(str)
    filtradas = df[df["IBGE"].str.startswith(ibge_codigo[:6])]
    if filtradas.empty:
        print(f"⚠️ Nenhuma UBS exata encontrada. Mostrando UBS do estado {uf}.")
        filtradas = df[df["UF"].str.upper() == uf.upper()]

    # 5️⃣ Calcular distância se houver coordenadas
    if lat_usuario and lon_usuario:
        filtradas["DISTANCIA_KM"] = filtradas.apply(
            lambda row: calcular_distancia(lat_usuario, lon_usuario, row["LATITUDE"], row["LONGITUDE"]),
            axis=1
        )
        filtradas = filtradas.sort_values("DISTANCIA_KM")

    # 6️⃣ Gerar resposta simples (somente nome + endereço)
    resultados = []
    for _, row in filtradas.head(5).iterrows():
        endereco = f"{row['LOGRADOURO']}, {row['BAIRRO']}, {cidade} - {uf}"
        resultados.append({
            "nome": row["NOME"],
            "endereco": endereco,
            "distancia_km": round(row["DISTANCIA_KM"], 2) if "DISTANCIA_KM" in row else None
        })

    resposta_final = {
        "cep": cep,
        "cidade": cidade,
        "uf": uf,
        "ubs_proximas": resultados
    }

    # 💾 7️⃣ Exportar JSON local (para histórico)
    try:
        with open("ubs_resultado.json", "w", encoding="utf-8") as f:
            json.dump(resposta_final, f, ensure_ascii=False, indent=4)
        print("💾 Dados exportados para ubs_resultado.json")
    except Exception as e:
        print(f"⚠️ Erro ao exportar JSON: {e}")

    return jsonify(resposta_final)

# 🚀 Execução principal
if __name__ == "__main__":
    print("🏥 API Consulta Certa - UBS iniciando com tratamento de erros...")
    print("Acesse: http://127.0.0.1:5000/ubs/perto?cep=01001000")
    app.run(debug=True)
