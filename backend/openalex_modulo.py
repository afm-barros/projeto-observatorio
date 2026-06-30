import requests
import urllib.parse

def buscar_pesquisadores_openalex(query: str, limite: int = 12):
    query_codificada = urllib.parse.quote(query)
    
    # Busca por Nome
    url = f"https://api.openalex.org/authors?filter=display_name.search:{query_codificada},last_known_institutions.country_code:br&sort=cited_by_count:desc&per_page={limite}"
    
    try:
        response = requests.get(url)
        if response.status_code != 200:
            return []
            
        dados = response.json()
        resultados_brutos = dados.get("results", [])
        
        # Busca Híbrida por Tema se não achou por nome
        if len(resultados_brutos) == 0:
            url_tema = f"https://api.openalex.org/authors?search={query_codificada}&filter=last_known_institutions.country_code:br&sort=cited_by_count:desc&per_page={limite}"
            response_tema = requests.get(url_tema)
            if response_tema.status_code == 200:
                resultados_brutos = response_tema.json().get("results", [])

        resultados = []
        for autor in resultados_brutos:
            temas_brutos = autor.get("x_concepts", [])
            temas_principais = [tema["display_name"] for tema in temas_brutos[:4]] if temas_brutos else ["Pesquisa Geral"]
            
            # --- NOVO: BUSCA OS ARTIGOS DO AUTOR ---
            works_url = autor.get("works_api_url")
            artigos_lista = []
            if works_url:
                # Pega os 5 artigos mais citados deste autor
                try:
                    res_works = requests.get(f"{works_url}?sort=cited_by_count:desc&per_page=5")
                    if res_works.status_code == 200:
                        obras = res_works.json().get("results", [])
                        for obra in obras:
                            # Simulando o Qualis aleatoriamente para fins visuais do projeto, já que OpenAlex não tem Qualis Capes nativo
                            import random
                            estratos = ["A1", "A2", "A3", "A4", "B1", "B2"]
                            qualis_mock = random.choice(estratos)
                            artigos_lista.append({
                                "titulo": obra.get("title", "Título indisponível"),
                                "qualis": qualis_mock
                            })
                except:
                    pass

            resultados.append({
                "nome": autor.get("display_name", "Pesquisador Desconhecido"),
                "indice_h": autor.get("summary_stats", {}).get("h_index", 0),
                "total_citacoes": autor.get("cited_by_count", 0),
                "temas": temas_principais,
                "artigos": artigos_lista # <-- Agora o pesquisador tem a lista de artigos
            })
            
        return resultados
    except Exception as e:
        print(f"Erro ao consultar OpenAlex: {e}")
        return []