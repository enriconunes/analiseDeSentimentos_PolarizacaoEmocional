import json
import spacy
from spacy import displacy
from collections import Counter

import string
import matplotlib.pyplot as plt

import nltk
from nltk.corpus import wordnet as wn
from nltk.corpus import sentiwordnet as swn
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords

# ARMAZENA O CONTEUDO DO FICHEIRO DENTRO DA VARIAVEL 'TWEETS'
file = open("jsonTeste.json", "r")
tweets = file.readlines()
file.close()

# criação de uma variavel do tipo String vazia que receberá todos os textos dos tweets
text = ""

for t in tweets:
    # se a linha for diferente de uma quebra de linha E se nao possuir a palavra 'limit'
    # (algumas linhas da base de dados apresentam a palavra 'limit', o que causa um erro na leitura)
    if (t != "\n" and (t.__contains__("limit") == False)):
        tweet = json.loads(t)
        # concatenação dos tweets em uma so variavel
        text = tweet["text"] + " " + text

for x in text.lower():  # REMOCAO DOS CARDINAIS DE TODOS OS TWEETS
    if x == "#":
        text = text.replace(x, "")

# utilização o método npl() para carregar os dados em inglês
nlp = spacy.load("en_core_web_sm")
doc = nlp(text)


array_entidades = []
# a funcao '.ents' retorna todas as entidades de um texto separadas em uma lista (array)
for entidades in doc.ents:
    # print(entidades, "|", entidades.label_)
    # adiciona 'entidades' que é um elemento do array retornado por 'doc.ents'
    array_entidades.append(entidades.text)

# print(array_entidades)

# array com todas as entidades
entidades_lower = []

# filtragem das entidades
allowed_chars = set(
    ("0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_-"))

# CRIA-SE UM NOVO ARRAY DE ENTIDADES SOMENTE COM CARACTERES PERMITIDOS E MINUSCULOS
for palavra in array_entidades:
    conferir = set((palavra))
    # REMOCAO DE EMOJIS e SINAIS
    # retorna True se todos os caracteres forem permitidos
    # issubset = confere se contem SÓ as letras permitidas (retorna true ou false)
    if conferir.issubset(allowed_chars):
        entidades_lower.append(palavra.lower())  # adiciona se for permitido
# print(entidades_lower)


# reducao do array com conjunto para eliminar os elementos repetidos e aumentar o desempenho
unica_entidade = set(entidades_lower)  # CONJUNTO -> REMOVE ELEMENTOS REPETIDOS
# print(unica_entidade)


# Criação dos arrays 'nome_entidade' e 'repeticao_entidade' que receberão o nome da entidade e quantidade de vezes que este nome se repete, respectivamente.
# Dessa forma, é possível identificar quais são as entidades que mais se repetem por meio do array 'repeticao_entidade' e, consequentemente, podemos acessar o seu nome(haja vista que nome_entidade[x] corresponde a repeticao_entidade[x]).
nome_entidade = []
repeticao_entidade = []

# ciclos para identificar a quantiade de vezes em que a entidade se repete.
# 'compara_entidade' percorre pelo conjunto 'unica_entidade' para comparar palavra por palavra do conjunto.
# 'palavra' percorre pelo array 'entidades_lower'. Se 'palavra' for igual a 'compara_entidade' (elemento do conjunto), entao acrescenta 1 ao contador.
for compara_entidade in unica_entidade:
    # o contador reseta sempre que for analisar uma nova palavra do conjunto.
    contador = 0
    for palavra in entidades_lower:
        if palavra == compara_entidade:
            contador = contador + 1
    # adiciona o nome da entidade em um array somente com nomes das entidades.
    nome_entidade.append(compara_entidade)
    # adiciona a quantidade de vezes em que a entidade se repete em um array somente com a quantidade de repetição .
    repeticao_entidade.append(contador)
    # O nome e a quantidade serao armazenados em arrays diferentes, porem, no mesmo indice em ambos os arrays.

# ou len(repeticao_entidade) (o tamanho dos arrays será sempre o mesmo).
# for x in range(len(nome_entidade)):
#     # Demonstração do armazenamento dos arrays
#     print("Entidade: %s   [Repeticoes: %5d]" % (nome_entidade[x].ljust(35, '.'), repeticao_entidade[x]))


# Ordenação do array de entidades(Ordenação: Entidade que se repete mais para a entidade que se repete menos). Método: BUBBLE SORT.
# IMPLEMENTACAO DO METODO BUBBLE SORT
# Com este método, é possível ordenar o array 'repeticao_entidade' e, junto com este array, o array 'nome_entidade' também se ordena

# inicia na ultima posicao (tamanho do array) e decresce um valor (-1) ate chegar em 0
for final in range(len(repeticao_entidade), 0, -1):
    for atual in range(0, final-1):
        # < indica que ordena na ordem decrescente
        if repeticao_entidade[atual] < repeticao_entidade[atual + 1]:
            repeticao_entidade[atual], repeticao_entidade[atual +
                                                          1] = repeticao_entidade[atual + 1], repeticao_entidade[atual]
            nome_entidade[atual], nome_entidade[atual +
                                                1] = nome_entidade[atual + 1], nome_entidade[atual]

# Ao fazer o print dos arrays novamente (como no bloco acima), é possivel ver que as entidades estão ordenadas de acordo com a qnt de repetição
# ou len(repeticao_entidade) (o tamanho dos arrays será sempre o mesmo).
# for x in range(len(nome_entidade)):
#     # Demonstração do armazenamento dos arrays
#     print("Entidade: %s   [Repeticoes: %5d]" % (
#         nome_entidade[x].ljust(35, '.'), repeticao_entidade[x]))


# Identificação das 10 entidades mais relevantes dos arrays lidos.
cnt_entidades_repetidas = 0

print("\n\n\n------------------------- TOP ENTIDADES -------------------------")
for x in range(len(nome_entidade)):
    print("TOP %2i: %s   [Repeticoes: %5d]" % (
        x+1, nome_entidade[x].ljust(35, '.'), repeticao_entidade[x]))
    cnt_entidades_repetidas += 1
    if (cnt_entidades_repetidas == 10):
        break
print("\n\n")
# ARMAZENANDO AS 10 ENTIDADES MAIS RELEVANTES EM UM ARRAY
top_entidades = []  # lista com as entidades mais relevantes em ordem decrescente

cnt = 0
for x in nome_entidade:
    if (cnt == 10):
        break
    top_entidades.append(x)
    cnt += 1
# print(top_entidades)

# IDENTIFICANDO TWEETS RELACIONADOS A CADA ENTIDADE
top_tweets = 10 * [""]

for t in tweets:
    # se a linha for diferente de uma quebra de linha E se nao possuir a palavra 'limit'
    # (algumas linhas da base de dados apresentam a palavra 'limit', o que causa um erro na leitura)
    if ((t.__contains__("limit") == False)):
        for index in range(10):
            if (t.lower().__contains__(top_entidades[index])):
                tweet = json.loads(t)
                # concatenação dos tweets em uma so variavel
                top_tweets[index] = tweet["text"] + " " + top_tweets[index]
# EXEMPLO:
# print(top_tweets[9])

# TOKENIZAÇÃO DOS TEXTOS COM NLTK E PASSANDO O TEXTO PARA LETRAS MINÚSCULAS
tokens_tweets = 10 * [""]

for x in range(10):
    tokens_tweets[x] = nltk.word_tokenize(top_tweets[x].lower())
# print(tokens_tweets[0])

# REMOVENDO STOP WORDS(palavras irrelevantes para a alise de sentimentos)
stop_words = set(stopwords.words('english'))

tokens_tweets_clean = 10 * [""]

for x in range(10):
    tokens_tweets_clean[x] = [
        word for word in tokens_tweets[x] if word not in stop_words]
# print("\nQuantidade de tokens dos tweets da primeira entidade sem a remocao das Stop Words: %i" % (len(tokens_tweets[0])))
# print("\nQuantidade de tokens dos tweets da primeira entidade com a remocao das Stop Words: %i" % (len(tokens_tweets_clean[0])))

# LEMATIZAÇÃO COM SENTIWORDNET (processo de deflexionar uma palavra para determinar o seu lema)
lemmatizador = WordNetLemmatizer()

# EXEMPLOS:
# print(lemmatizador.lemmatize("dogs"))
# print(lemmatizador.lemmatize("cats"))
# print(lemmatizador.lemmatize("loves"))
# print(lemmatizador.lemmatize("wants"))
tokens_lematizados = 10 * [""]

for x in range(10):
    tokens_lematizados[x] = [lemmatizador.lemmatize(
        word) for word in tokens_tweets_clean[x]]


# POS TAGGING (Etiquetar cada token com a sua classificação gramatical) UTILIZANDO NLTK
tokens_tag = 10 * [""]

for x in range(10):
    tokens_tag[x] = nltk.pos_tag(tokens_lematizados[x])

# EXEMPLO DAS TAGS
# print(tokens_tag[0])

# VARIÁVEIS PARA RECEBER A PONTUACAO DE POLARIDADE DE CADA INDICE DA LISTA
pos = 10 * [0]
neg = 10 * [0]
obj = 10 * [0]
count = 10 * [0]


# IDENTIFICAÇÃO DOS VERBOS QUE SE REPETIRAM MAIS EM CADA INDICE DA LISTA DE TWEETS
# allowed_chars = set(("0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_-")) <- Variavel ja declarada anteriormente

verbos_entidades = 10 * [""]

for x in range(10):
    verbos = []
    for (palavra, tag) in tokens_tag[x]:
        # adiciona apenas se o token tiver a tag 'VB' e nao conter emoji/sinais
        if (tag == "VB" and set(palavra).issubset(allowed_chars)):
            verbos.append(palavra)
    verbos_entidades[x] = verbos

# print(top_verbos[0])

conjunto_verbo = 10 * [0]

for x in range(10):
    conjunto_verbo[x] = set(verbos_entidades[x])

top_verbos = [], [], [], [], [], [], [], [], [], []

for x in range(10):
    for compara_verbo in conjunto_verbo[x]:
        contador = 0
        for verbo in verbos_entidades[x]:
            if (verbo == compara_verbo):
                contador = contador + 1
        top_verbos[x].append((contador, compara_verbo))


for index in range(10):
    top_verbos[index].sort(reverse=True)  # organizacao decrescente

print("\n\n------------------------- VERBALIZACAO -------------------------")
for index in range(10):
    contador_verbos = 0
    print("\n10 Verbos mais presentes da entidade ->", top_entidades[index])
    for (x, y) in top_verbos[index]:
        if (contador_verbos == 10):
            break
        print("Verbo: %s   [Repeticoes: %5d]" % (y.ljust(35, '.'), x))
        contador_verbos += 1


# FUNÇÕES PARA O SCORING DE SENTIMENTOS
# Conversão entre Tags do Penn Treebank para as Tags simples do wordnet
def penn_para_wn(tag):
    if tag.startswith("J"):
        return wn.ADJ
    elif tag.startswith("N"):
        return wn.NOUN
    elif tag.startswith("R"):
        return wn.ADV
    elif tag.startswith("V"):
        return wn.VERB
    return None


def obter_sentimento(word, tag):
    wn_tag = penn_para_wn(tag)
    # print("Tag Penn Treebank: ", tag)
    # print("Tag Wordnet:", wn_tag)

    # SYNSET: grupos de sinonimos que expressam o mesmo significado
    synsets = wn.synsets(word, pos=wn_tag)
    if not synsets:
        return []

    # PEGAR O PRIMEIRO SENTIDO
    synset = synsets[0]
    swn_synset = swn.senti_synset(synset.name())
    return [synset.name(), swn_synset.pos_score(), swn_synset.neg_score(), swn_synset.obj_score()]


# UTILIZAÇÃO DAS FUNÇÕES PARA A OBTENÇÃO DOS SYNSETS COM SUAS RESPECTIVAS PONTUAÇÕES(pos, neg e obj)
senti_val = 10 * [0]
for x in range(10):
    senti_val[x] = [obter_sentimento(x, y) for (x, y) in tokens_tag[x]]


# CÁLCULO DA MÉDIA DA PONTUAÇÃO DE CADA ENTIDADE
qntd = 10 * [0]
for x in range(10):
    for i in range(len(senti_val[x])):
        try:
            # Exclusao das palavras em que o OBJ seja == 1 (Palavras com sentimentos neutros)
            if (senti_val[x][i][3] != 1):
                pos[x] = pos[x] + senti_val[x][i][1]
                neg[x] = neg[x] + senti_val[x][i][2]
                obj[x] = obj[x] + senti_val[x][i][3]
                qntd[x] = qntd[x] + 1
                # print para analise dos dados
                # print(senti_val[x][i])
        except:
            continue
total_pontuacao = 10 * [0]
for x in range(10):
    # MÉDIA: Soma de todos os numeros positivos dividido pela quantidade de numeros somados
    pos[x] = pos[x] / qntd[x]
    neg[x] = neg[x] / qntd[x]
    # valores positivos - valores positivos
    total_pontuacao[x] = pos[x] - neg[x]

print("\n\nPONTUACAO:\n")
print("     ENTIDADE             POSITIVO            NEGATIVO            TOTAL:")
for x in range(10):
    print("%2dº  %s %f            %f            %f" % (
        x+1, top_entidades[x].ljust(20, " "), pos[x], neg[x], total_pontuacao[x]))
print("\n\n")

# CRIAÇÃO DO GRÁFICO PARA A REPRESENTAÇÃO DAS 10 ENTIDADES MAIS COMENTADAS E SUAS RESPECTIVAS POLARIDADES (ENTRE -1 E 1)
fig, ax1 = plt.subplots()
ax1.bar(top_entidades, total_pontuacao)
ax1.set_title(
    "\n\n10 ENTIDADES MAIS COMENTADAS E SUAS POLARIDADES EMOCIONAIS\n\n")
plt.ylim(-1, 1)
plt.grid(True)
fig.autofmt_xdate()
