
import csv
import os
import db_config 

def exportar_para_csv():
    print("--- Iniciando exportação para CSV ---")
    
    if not db_config.init_db_pool():
        print("Erro ao conectar no banco.")
        return

    print("Baixando dados do Oracle...")
    dados_lista = db_config.buscar_dados_relatorio_db()
    
    if not dados_lista:
        print("Nenhum dado encontrado.")
        return

    nome_arquivo = "dados_gs_ecofloor.csv"

    pasta_backend = os.path.dirname(os.path.abspath(__file__))
    
   
    caminho_completo = os.path.join(pasta_backend, "..", "data", nome_arquivo)

    try:
        
        with open(caminho_completo, mode='w', newline='', encoding='utf-8') as arquivo_csv:
            
            colunas = dados_lista[0].keys()
            writer = csv.DictWriter(arquivo_csv, fieldnames=colunas)
            
            writer.writeheader()
            writer.writerows(dados_lista)
            
        # os.path.abspath mostra o caminho bonitinho na tela 
        print(f"\n✅ SUCESSO! Arquivo salvo em:\n{os.path.abspath(caminho_completo)}")
        print(f"Total de linhas: {len(dados_lista)}")
        
    except Exception as e:
        print(f"Erro ao criar arquivo CSV: {e}")

if __name__ == "__main__":
    exportar_para_csv()