# Importa a conexão Singleton do banco de dados
from banco import conexao_singleton as cs

# Obtém uma instância de conexão com o banco de dados
conexao = cs.Conexao().get_conexao()

def salvar_nova_producao(id: str, pesquisador_id: str, nomeartigo: str) -> str:
    # Ignoramos o ID passado, pois o banco gera automaticamente
    sql = "INSERT INTO producoes (pesquisador_id, nomeartigo) VALUES (%s, %s)"
    try:
        with conexao.cursor() as cursor:
            cursor.execute(sql, (pesquisador_id, nomeartigo))
            conexao.commit()
            return "Produção salva com sucesso!"
    except Exception as e:
        conexao.rollback()
        return f"Erro ao salvar: {e}"

def listar_todas() -> list:
    sql = "SELECT * FROM producoes"
    with conexao.cursor() as cursor:
        cursor.execute(sql)
        resultado = cursor.fetchall()
        if not resultado: return []
        colunas = [desc[0] for desc in cursor.description]
        return [dict(zip(colunas, linha)) for linha in resultado]

# A FUNÇÃO DE OURO (Requisito 3 do PDF)
def listar_por_pesquisador(pesquisador_id: str) -> list:
    sql = "SELECT * FROM producoes WHERE pesquisador_id = %s"
    try:
        with conexao.cursor() as cursor:
            cursor.execute(sql, (pesquisador_id,))
            resultado = cursor.fetchall()
            if not resultado: return []
            colunas = [desc[0] for desc in cursor.description]
            return [dict(zip(colunas, linha)) for linha in resultado]
    except Exception as e:
        conexao.rollback()
        return []

def atualizar_por_id(id: str, pesquisador_id: str, nomeartigo: str) -> str:
    sql = "UPDATE producoes SET pesquisador_id = %s, nomeartigo = %s WHERE id = %s"
    try:
        with conexao.cursor() as cursor:
            cursor.execute(sql, (pesquisador_id, nomeartigo, id))
            conexao.commit()
            return "Produção atualizada com sucesso!"
    except Exception as e:
        conexao.rollback()
        return f"Erro ao atualizar: {e}"

def apagar_por_id(id: str) -> str:
    sql = "DELETE FROM producoes WHERE id = %s"
    try:
        with conexao.cursor() as cursor:
            cursor.execute(sql, (id,))
            conexao.commit()
            return "Produção apagada com sucesso!"
    except Exception as e:
        conexao.rollback()
        return f"Erro ao apagar: {e}"