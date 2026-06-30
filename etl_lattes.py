import xml.etree.ElementTree as ET
import csv
import os

arquivos_xml = ['6716225567627323.xml', '1966167015825708.xml']
tabela_pesquisadores = []
tabela_producoes = []

pesquisador_id_counter = 1
producoes_id_counter = 1

print("Iniciando a extração de dados (Modo Dupla Ativado)...\n")

for arquivo in arquivos_xml:
    if not os.path.exists(arquivo):
        print(f"Erro: Arquivo {arquivo} não encontrado na pasta.")
        continue

    tree = ET.parse(arquivo)
    root = tree.getroot()

    dados_gerais = root.find('DADOS-GERAIS')
    nome = dados_gerais.get('NOME-COMPLETO')
    lattes_id = root.get('NUMERO-IDENTIFICADOR')

    tabela_pesquisadores.append({
        'pesquisador_id': pesquisador_id_counter,
        'lattesid': lattes_id,
        'nome': nome
    })
    
    print(f"Pesquisador encontrado: {nome} (ID: {pesquisador_id_counter})")

    artigos_publicados = root.find('.//ARTIGOS-PUBLICADOS')
    
    if artigos_publicados is not None:
        for artigo in artigos_publicados.findall('ARTIGO-PUBLICADO'):
            dados_basicos = artigo.find('DADOS-BASICOS-DO-ARTIGO')
            detalhamento = artigo.find('DETALHAMENTO-DO-ARTIGO')
            
            if dados_basicos is not None:
                ano = dados_basicos.get('ANO-DO-ARTIGO')
                titulo = dados_basicos.get('TITULO-DO-ARTIGO')
                issn = detalhamento.get('ISSN') if detalhamento is not None else 'N/A'
                
                if ano and 2020 <= int(ano) <= 2024:
                    tabela_producoes.append({
                        'producoes_id': producoes_id_counter,
                        'pesquisador_id': pesquisador_id_counter,
                        'anoartigo': ano,
                        'nomeartigo': titulo,
                        'issn': issn
                    })
                    producoes_id_counter += 1

    pesquisador_id_counter += 1

with open('tabela_pesquisadores.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['pesquisador_id', 'lattesid', 'nome'])
    writer.writeheader()
    writer.writerows(tabela_pesquisadores)

with open('tabela_producoes.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['producoes_id', 'pesquisador_id', 'anoartigo', 'nomeartigo', 'issn'])
    writer.writeheader()
    writer.writerows(tabela_producoes)

print("\nExtração concluída com sucesso! Minério refinado.")
print("Arquivos 'tabela_pesquisadores.csv' e 'tabela_producoes.csv' criados.")
