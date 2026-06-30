-- 1. Cria uma coluna dedicada na tabela de produções para armazenar os vetores de texto
ALTER TABLE public.producoes 
ADD COLUMN IF NOT EXISTS vetor_busca tsvector 
GENERATED ALWAYS AS (to_tsvector('portuguese', coalesce(nomeartigo, ''))) STORED;

-- 2. Cria um índice GIN para garantir que a pesquisa seja imediata e otimizada
CREATE INDEX IF NOT EXISTS idx_fts_producoes ON public.producoes USING GIN (vetor_busca);

-- 3. Executa a busca real testando os termos "saúde" OU "tecnologia" e calcula a relevância
SELECT 
    p.nome AS pesquisador,
    pr.nomeartigo AS artigo,
    ts_rank(pr.vetor_busca, to_tsquery('portuguese', 'saúde | tecnologia')) AS relevancia
FROM 
    public.producoes pr
JOIN 
    public.pesquisadores p ON pr.pesquisador_id = p.pesquisador_id
WHERE 
    pr.vetor_busca @@ to_tsquery('portuguese', 'saúde | tecnologia')
ORDER BY 
    relevancia DESC;