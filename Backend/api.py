# Em Backend/api.py
from flask import Flask, jsonify, request
import db_config
from ML import classificar_desperdicio

app = Flask(__name__)

@app.route('/api/dados_sensor', methods=['POST'])
def receber_dados_sensor():
    dados = request.json

    if not dados or 'sala_id' not in dados:
        return jsonify({"erro": "Dados inválidos"}), 400
    
    print(f"\n[API]: Dados recebidos do Wokwi: {dados}")

    # 1. Salva no banco
    db_config.salvar_log_sensor(dados)

    # 2. Roda a IA para classificar o status atual
    Class = classificar_desperdicio(dados)
    sala_id = dados.get('sala_id')
    temp_atual = dados.get('temperatura', 20)

    # --- LÓGICA DE DECISÃO ---
    
    # Estado padrão: Mantém o que o Wokwi mandou
    comando_luz = "ON" if dados.get('luz_ligada') else "OFF"
    comando_ac = "ON" if dados.get('ac_ligado') else "OFF"

    # Lógica da LUZ
    if Class == "DESPERDICIO_LUZ":
        comando_luz = "OFF"
    elif Class == "OK" and dados.get('presenca'):
        comando_luz = "ON"

    # Lógica do AR CONDICIONADO
    # Regra 1: Termostato (Se tiver gente e calor > 23, liga
    if temp_atual > 23:
        comando_ac = "ON"
    else:
        comando_ac = "OFF" # Se < 23, desliga para economizar

    # Regra 2: Prioridade Absoluta (Se ML disse que é desperdício, desliga tudo)
    # Isso cobre sala vazia OU sala fria demais com ar ligado
    if Class == "DESPERDICIO_AC" or dados.get('presenca') == False:
        comando_ac = "OFF"
    
    # 3. Atualiza o comando no banco para o Wokwi ler depois
    db_config.atualizar_comando_sala_db(sala_id, comando_luz, comando_ac)

    return jsonify({"status": "recebido"}), 201

@app.route('/api/comandos/<sala_id>', methods=['GET'])
def envia_comandos_atuador(sala_id):
    print(f"\n[API]: Wokwi (Atuador) solicitou comandos para a sala {sala_id}")
    comandos = db_config.buscar_comando_sala_db(sala_id)
    return jsonify(comandos), 200

@app.route('/api/relatorio', methods=['GET'])
def envia_dados_relatorio():
    print(f"\n[API]: Script R pedindo relatório")
    dados_totais = db_config.buscar_dados_relatorio_db()
    return jsonify(dados_totais), 200

if __name__ == '__main__':
    # Inicia o banco
    if db_config.init_db_pool():
        print("\n--- Conexão com Oracle OK. Iniciando API... ---")
        print(app.url_map)
        app.run(host='0.0.0.0', port=5000, debug=True)
    else:
        print("Erro crítico ao conectar no banco. Verifique .env")