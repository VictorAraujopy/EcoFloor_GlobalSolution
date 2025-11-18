# Em Backend/ML.py
# (Código da Pessoa 5)

def classificar_desperdicio(dados_sensor):
    """
    Classifica os dados do sensor como 'DESPERDICIO' ou 'OK'.
    """
    presenca = dados_sensor.get('presenca')
    luz_ligada = dados_sensor.get('luz_ligada')
    ac_ligado = dados_sensor.get('ac_ligado')

    # REGRA 1: Desperdício de Luz
    if presenca == False and luz_ligada == True:
        return "DESPERDICIO_LUZ"
    
    # REGRA 2: Desperdício de Ar Condicionado
    if presenca == False and ac_ligado == True:
        return "DESPERDICIO_AC"

    # Se não houver desperdício (ou se tiver gente)
    return "OK"