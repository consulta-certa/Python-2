from flask import Flask, request, jsonify
import requests
import pandas as pd
import os
import json
from math import radians, sin, cos, sqrt, atan2

app = Flask(__name__)
CSV_PATH = "Unidades_Basicas_Saude-UBS.csv"

def calcular_distancia(lat1, lon1, lat2, lon2):
    """Calcula a distância entre dois pontos geográficos (em km) usando a fórmula de Haversine."""
    R = 6371  # Raio médio da Terra em km
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c


@app.route("/ubs/perto", methods=["GET"])
def buscar_ubs():
    """Busca UBS próximas com base no CEP informado."""
    cep = request.args.get("cep")
    if not cep:
        return jsonify({"erro": "CEP não informado"}), 400

    print(f"\n🔍 Buscando UBS para o CEP: {cep}")

    # 1️⃣ Consulta o ViaCEP para obter cidade, UF e IBGE
    via_cep_url = f"https://viacep.com.br/ws/{cep}/json/"
    resposta = requests.get(via_cep_url)

    if resposta.status_code != 200:
        return jsonify({"erro": "Erro ao consultar o ViaCEP"}), 500

    dados_cep = resposta.json()
    cidade = dados_cep.get("localidade")
    uf = dados_cep.get("uf")
    ibge_codigo = dados_cep.get("ibge")

    if not cidade or not uf or not ibge_codigo:
        return jsonify({"erro": "CEP inválido ou sem código IBGE"}), 400

    print(f"🏙️ Cidade identificada: {cidade} ({uf}), IBGE: {ibge_codigo}")

    # 🗺️ Obter latitude e longitude do CEP usando Nominatim
    nominatim_url = f"https://nominatim.openstreetmap.org/search?postalcode={cep}&country=Brazil&format=json"
    resp_coord = requests.get(nominatim_url, headers={"User-Agent": "consulta-certa-app"})
    if resp_coord.status_code == 200 and resp_coord.json():
        localizacao = resp_coord.json()[0]
        lat_usuario = float(localizacao["lat"])
        lon_usuario = float(localizacao["lon"])
        print(f"📍 Localização aproximada do usuário: {lat_usuario}, {lon_usuario}")
    else:
        lat_usuario = lon_usuario = None
        print("⚠️ Não foi possível obter coordenadas do CEP.")

    # 2️⃣ Verifica se o CSV existe
    if not os.path.exists(CSV_PATH):
        return jsonify({"erro": "Arquivo CSV com UBS não encontrado"}), 500

    # 3️⃣ Lê o CSV
    try:
        df = pd.read_csv(CSV_PATH, sep=";", dtype=str)
    except Exception as e:
        return jsonify({"erro": f"Falha ao ler o CSV: {e}"}), 500

    # Corrige vírgulas nos decimais
    df["LATITUDE"] = df["LATITUDE"].str.replace(",", ".", regex=False).astype(float)
    df["LONGITUDE"] = df["LONGITUDE"].str.replace(",", ".", regex=False).astype(float)

    # 4️⃣ Filtra UBS do mesmo município via código IBGE
    df["IBGE"] = df["IBGE"].astype(str)
    filtradas = df[df["IBGE"].str.startswith(ibge_codigo[:6])]

    # 5️⃣ Se não encontrar, usa fallback pelo UF
    if filtradas.empty:
        print(f"⚠️ Nenhuma UBS encontrada com IBGE {ibge_codigo}. Retornando UBS do estado {uf}.")
        filtradas = df[df["UF"].str.upper() == uf.upper()].head(10)
    else:
        print(f"✅ {len(filtradas)} UBS encontradas para {cidade} ({uf}).")

    # 6️⃣ Calcula distância (somente para ordenar)
    if lat_usuario and lon_usuario:
        filtradas["DISTANCIA_KM"] = filtradas.apply(
            lambda row: calcular_distancia(
                lat_usuario, lon_usuario,
                row["LATITUDE"], row["LONGITUDE"]
            ),
            axis=1
        )
        filtradas = filtradas.sort_values("DISTANCIA_KM")
    else:
        filtradas["DISTANCIA_KM"] = None

    # 7️⃣ Monta o JSON de resposta
    resultados = filtradas.head(5)[["NOME", "BAIRRO", "LATITUDE", "LONGITUDE"]].to_dict(orient="records")

    resposta_final = {
        "fonte": "CSV local (IBGE + proximidade)",
        "cep": cep,
        "cidade": cidade,
        "uf": uf,
        "ibge": ibge_codigo,
        "ubs_proximas": resultados
    }

    # 💾 8️⃣ Exporta o resultado da consulta para JSON local
    with open("ubs_resultado.json", "w", encoding="utf-8") as f:
        json.dump(resposta_final, f, ensure_ascii=False, indent=4)

    print("💾 Dados exportados para ubs_resultado.json")
    return jsonify(resposta_final)


if __name__ == "__main__":
    print("🏥 API Consulta Certa - UBS iniciando com cálculo de proximidade geográfica...")
    print("Acesse: http://127.0.0.1:5000/ubs/perto?cep=01001000")
    app.run(debug=True)
