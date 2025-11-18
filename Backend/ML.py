# Em Backend/ML.py

def classificar_desperdicio(dados_sensor):
    """
    Classifica os dados do sensor como 'DESPERDICIO' ou 'OK'.
    """
    presenca = dados_sensor.get('presenca')
    luz_ligada = dados_sensor.get('luz_ligada')
    ac_ligado = dados_sensor.get('ac_ligado')
    
    # Pega a temperatura (se não vier, assume 25 pra não dar erro)
    temperatura = dados_sensor.get('temperatura', 25) 

    # REGRA 1: LUZ
    # Luz ligada sem ninguém = DESPERDÍCIO
    if presenca == False and luz_ligada == True:
        return "DESPERDICIO_LUZ"
    
    # REGRA 2: AR CONDICIONADO
    if ac_ligado == True:
        # Caso A: Ar ligado sem ninguém na sala (Clássico)
        if presenca == False:
            return "DESPERDICIO_AC"
            
        # Caso B: Ar ligado com gente, MAS está frio (< 23 graus)
        # Isso é desperdício técnico!
        if temperatura < 23:
            return "DESPERDICIO_AC"

    # Se passou por tudo e não caiu nos ifs, tá tudo certo.
    return "OK"