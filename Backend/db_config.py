# Em Backend/db_config.py
import oracledb
import os
from dotenv import load_dotenv

load_dotenv()
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_DSN = os.getenv("DB_DSN")

pool = None 

def init_db_pool():
    global pool
    try:
        print("[DB CONFIG] Iniciando Pool de Conexões...")
        pool = oracledb.create_pool(user=DB_USER, password=DB_PASS, dsn=DB_DSN, min=2, max=5, increment=1)
        print("[DB CONFIG] Pool de Conexões criado com SUCESSO.")
        return True
    except Exception as e:
        print(f"[DB CONFIG] ERRO AO CRIAR POOL: {e}")
        return False

def salvar_log_sensor(dados):
    """
    (INSERT) Salva os dados, incluindo TEMPERATURA.
    """
    sql = """
        INSERT INTO logs_sensores (sala_id, presenca, luz_ligada, ac_ligado, temperatura)
        VALUES (:1, :2, :3, :4, :5)
    """
    
    dados_para_banco = (
        dados.get('sala_id'),
        1 if dados.get('presenca') else 0,
        1 if dados.get('luz_ligada') else 0,
        1 if dados.get('ac_ligado') else 0,
        dados.get('temperatura', 0) # Salva 0 se não vier temperatura
    )
    try:
        with pool.acquire() as connection:
            with connection.cursor() as cursor:
                cursor.execute(sql, dados_para_banco)
                connection.commit()
        print(f"[DB INSERT] Log salvo: {dados_para_banco}")
    except Exception as e:
        print(f"[DB ERRO - INSERT]: {e}")

def atualizar_comando_sala_db(sala_id, comando_luz, comando_ac):
    sql = """
        MERGE INTO status_salas s
        USING (SELECT :1 AS sala_id, :2 AS luz, :3 AS ac FROM DUAL) d
        ON (s.sala_id = d.sala_id)
        WHEN MATCHED THEN
            UPDATE SET s.comando_luz = d.luz, s.comando_ac = d.ac
        WHEN NOT MATCHED THEN
            INSERT (sala_id, comando_luz, comando_ac)
            VALUES (d.sala_id, d.luz, d.ac)
    """
    dados_tuple = (sala_id, comando_luz, comando_ac)
    try:
        with pool.acquire() as connection:
            with connection.cursor() as cursor:
                cursor.execute(sql, dados_tuple)
                connection.commit()
        print(f"[DB MERGE] Status atualizado: Sala {sala_id} -> Luz={comando_luz}, AC={comando_ac}")
    except Exception as e:
        print(f"[DB ERRO - MERGE]: {e}")

def buscar_comando_sala_db(sala_id):
    sql = "SELECT comando_luz, comando_ac FROM status_salas WHERE sala_id = :1"
    try:
        with pool.acquire() as connection:
            with connection.cursor() as cursor:
                cursor.execute(sql, [sala_id])
                row = cursor.fetchone()
                if row:
                    return {"luz_comando": row[0], "ac_comando": row[1]}
                else:
                    return {"luz_comando": "OFF", "ac_comando": "OFF"}
    except Exception as e:
        print(f"[DB ERRO - SELECT]: {e}")
        return {"luz_comando": "OFF", "ac_comando": "OFF"}

def buscar_dados_relatorio_db():
    sql = "SELECT sala_id, presenca, luz_ligada, ac_ligado, temperatura, TO_CHAR(timestamp, 'YYYY-MM-DD HH24:MI:SS') AS timestamp_str FROM logs_sensores"
    try:
        with pool.acquire() as connection:
            with connection.cursor() as cursor:
                cursor.execute(sql)
                cols = [d[0].lower() for d in cursor.description]
                rows = cursor.fetchall()
                result_list = [dict(zip(cols, row)) for row in rows]
                return result_list
    except Exception as e:
        print(f"[DB ERRO - SELECT *]: {e}")
        return []