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
    


    db_config.salvar_log_sensor(dados)
    #Roda a IA
    Class = classificar_desperdicio(dados)
    #Pega o ID da sala
    sala_id = dados.get('sala_id')

    comando_luz = "ON" if dados.get('luz_ligada') else "OFF"
    comando_ac = "ON" if dados.get('ac_ligado') else "OFF"

    if Class == "DESPERDICIO_LUZ":
        comando_luz = "OFF"

    elif Class == "DESPERDICIO_AC":
        comando_ac = "OFF"
    
    elif Class == "OK" and dados.get('presenca'):
        comando_luz = "ON"
        comando_ac = "ON"
    db_config.atualizar_comando_sala_db(sala_id, comando_luz, comando_ac)

    return jsonify({"status": "recebido"}), 201

@app.route('/api/comandos/<sala_id>', methods=['GET'])

def envia_comandos_atuador(sala_id):
  print (f"\n[API]: Wokwi (Atuador) solicitou comandos para a sala {sala_id}")

  comandos = db_config.buscar_comando_sala_db(sala_id)

  return jsonify(comandos), 200

def envia_dados_relatorio():
    print(f"\n[API]: Script R pedindo relatório")

    return jsonify({"dados_totais"}), 200


if __name__ == '__main__':
    # ADICIONE ISSO AQUI 👇
    print("\n--- ROTAS REGISTRADAS ---")
    print(app.url_map)
    print("-------------------------\n")
    
    app.run(host='0.0.0.0', port=5000, debug=True)