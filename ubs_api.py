from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route("/ubs/perto", methods=["GET"])
def buscar_ubs():
    cep = request.args.get("cep")
    if not cep:
        return jsonify({"erro": "CEP não informado"}), 400

    # 1️⃣ Buscar cidade a partir do CEP
    via_cep_url = f"https://viacep.com.br/ws/{cep}/json/"
    resposta = requests.get(via_cep_url)
    if resposta.status_code != 200:
        return jsonify({"erro": "Erro ao consultar CEP"}), 500

    dados_cep = resposta.json()
    cidade = dados_cep.get("localidade")
    uf = dados_cep.get("uf")

    if not cidade or not uf:
        return jsonify({"erro": "CEP inválido"}), 400

    # 2️⃣ Buscar UBS na cidade com Nominatim (OpenStreetMap)
    query = f"UBS {cidade} {uf}"
    nominatim_url = f"https://nominatim.openstreetmap.org/search?q={query}&format=json&limit=5"
    resposta_ubs = requests.get(nominatim_url, headers={"User-Agent": "consulta-certa-app"})

    if resposta_ubs.status_code != 200:
        return jsonify({"erro": "Erro ao consultar API de locais"}), 500

    ubs_lista = resposta_ubs.json()
    resultados = [
        {
            "nome": item.get("display_name"),
            "latitude": item.get("lat"),
            "longitude": item.get("lon")
        }
        for item in ubs_lista
    ]

    return jsonify({
        "cep": cep,
        "cidade": cidade,
        "uf": uf,
        "ubs_proximas": resultados
    })

if __name__ == "__main__":
    app.run(debug=True)
