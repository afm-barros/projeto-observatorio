import nltk
from nltk.corpus import stopwords
from nltk.stem import RSLPStemmer
from nltk.tokenize import word_tokenize

# 1. Baixar os dicionários e regras do NLTK (Necessário apenas na primeira vez)
nltk.download('punkt_tab')
nltk.download('stopwords')
nltk.download('rslp')

# 2. Simulando um título de artigo vindo do seu banco de dados
texto_original = "SAÚDE PÚBLICA: PROSPECÇÃO TECNOLÓGICA DOS REGISTROS DE SOFTWARES PARA O COMBATE A DENGUE"
texto_minusc = texto_original.lower()

# 3. Tokenização: O NLTK quebra a frase inteira em uma lista de palavras
palavras = word_tokenize(texto_minusc, language='portuguese')

# 4. Remoção de Stop Words: Tirando conectivos inúteis para a busca (de, para, o, a)
stop_words_pt = set(stopwords.words('portuguese'))
palavras_sem_stop = [palavra for palavra in palavras if palavra not in stop_words_pt]

# 5. Stemming: Reduzindo as palavras ao seu radical (ex: tecnológica vira tecnolog)
stemmer = RSLPStemmer()
palavras_stemizadas = [stemmer.stem(palavra) for palavra in palavras_sem_stop]

# 6. Exibindo os resultados no terminal
print("\n--- PROCESSAMENTO DE LINGUAGEM NATURAL (NLTK) ---")
print(f"Texto Original: {texto_original}\n")
print(f"A. Tokens (Palavras separadas): {palavras}")
print(f"B. Sem Stop Words (Filtro limpo): {palavras_sem_stop}")
print(f"C. Stemming (Raízes para busca): {palavras_stemizadas}\n")