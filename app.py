
from flask import Flask, jsonify, request
from datetime import datetime
import json
import os

app = Flask(__name__)

ARQUIVO = 'alertas.json'

def carregar_alertas():
    if os.path.exists(ARQUIVO):
        with open(ARQUIVO, 'r') as f:
            return json.load(f)
    return []

def salvar_alertas(alertas):
    with open(ARQUIVO, 'w') as f:
        json.dump(alertas, f, indent=4)

alertas = carregar_alertas()

@app.route('/alertas', methods=['GET'])
def listar_alertas():
    return jsonify(alertas)

@app.route('/alertas', methods=['POST'])
def adicionar_alerta():
    dados = request.get_json()
    novo_alerta = {
        'id': len(alertas) + 1,
        'localizacao': dados.get('localizacao'),
        'descricao': dados.get('descricao'),
        'data_hora': datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    }
    alertas.append(novo_alerta)
    salvar_alertas(alertas)
    return jsonify({'mensagem': 'Alerta cadastrado com sucesso!', 'alerta': novo_alerta}), 201

@app.route('/', methods=['GET'])
def home():
    return "API de Alertas de Alagamento está rodando!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
