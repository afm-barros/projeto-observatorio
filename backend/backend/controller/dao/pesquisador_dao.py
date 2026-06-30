# Importa a conexão Singleton do banco de dados
from banco import conexao_singleton as cs

# Obtém uma instância de conexão com o banco de dados
conexao = cs.Conexao().get_conexao()

# Função para salvar um novo pesquisador no banco de dados
def salvar_novo_pesquisador(nome: str, lattes_id: str) -> str:
    # Corrigido para a coluna real do banco: lattesid (sem underline)
    sql = "INSERT INTO pesquisadores (lattesid, nome) VALUES (%s, %s)"
    
    try:
        with conexao.cursor() as cursor:
            cursor.execute(sql, (lattes_id, nome))
            conexao.commit()
            return "Novo pesquisador salvo com sucesso!"
    except Exception as e:
        conexao.rollback()
        return f"Erro ao salvar: {e}"
    
# Função para listar todos os pesquisadores do banco de dados
def listar_todos() -> list:
    # Usamos o AS para enganar o FastAPI e entregar os nomes que ele exige
    sql = "SELECT pesquisador_id AS pesquisadores_id, lattesid AS lattes_id, nome FROM pesquisadores"
    
    with conexao.cursor() as cursor:
        cursor.execute(sql)
        resultado = cursor.fetchall()
        
        # Cria uma lista das colunas retornadas pela consulta
        colunas = [desc[0] for desc in cursor.description]
        # Mapeia os resultados em dicionários com chave-valor
        dados = [dict(zip(colunas, linha)) for linha in resultado]
        
        return dados

# Função para atualizar um pesquisador no banco de dados com base no "lattes_id"
def atualizar_por_id(nome: str, pesquisadores_id: str, lattes_id: str) -> str:
    # Ajustado para os nomes reais das colunas no banco: pesquisador_id e lattesid
    sql = "UPDATE pesquisadores SET nome = %s, pesquisador_id = %s WHERE lattesid = %s"
    
    try:
        with conexao.cursor() as cursor:
            cursor.execute(sql, (nome, pesquisadores_id, lattes_id))
            
            if cursor.rowcount == 0:
                raise Exception("Nenhum registro encontrado para atualizar.")
            
            conexao.commit()
            return "Pesquisador atualizado com sucesso!"
    except Exception as e:
        conexao.rollback()
        return f"Erro ao atualizar pesquisador: {e}"

# Função para apagar um pesquisador do banco de dados com base no "lattes_id"
def apagar_por_lattes_id(lattes_id: str) -> str:
    # Corrigido para a coluna real do banco: lattesid
    sql = "DELETE FROM pesquisadores WHERE lattesid = %s"
    
    try:
        with conexao.cursor() as cursor:
            cursor.execute(sql, (lattes_id, ))
            
            if cursor.rowcount > 0:
                conexao.commit()
                return "Pesquisador apagado com sucesso!"
            else:
                raise Exception("Pesquisador inexistente ou ID inválido.")
    except Exception as e:
        conexao.rollback()
        return f"Erro ao apagar pesquisador: {e}"