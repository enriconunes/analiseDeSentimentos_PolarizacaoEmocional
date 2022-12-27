# processamentoDeLinguagemNatural_Python
Análise de 5.000 tweets (Json) para o Processamento de linguagem natural (NLP) com Python

Esta aplicação foi desenvolvida no objetivo de analisar a Polarização Emocional de 10 ´trends´ (entidades que mais se repetem no dataset), que pode variar de -1 (muito negativo) e 1 (muito positivo), onde 0 é um sentimento neutro. Para isso, é utilizado um dataset do tipo Json baixado pelo site Kaggle (https://www.kaggle.com/datasets/xvivancos/tweets-during-r-madrid-vs-liverpool-ucl-2018) contendo 10000 linhas, cerca de 5.000 tweets. Os passos que a aplicação segue para realizar esta atividade é:

1º. Identificar as 10 entidades mais comentadas entre os 5.000 tweets utilizando a biblioteca spacy <br/>
2º. Identificar e agrupar os tweets que contém cada entidade em um array com 10 índices, onde cada índice corresponde à todos os tweets de cada entidade.
3º. Tokenização dos tweets recolhidos com a função nltk.word_tokenize
4º. Remoçao das stop words dos tokens usando a biblioteca nltk.corpus
5º. Lematização dos tokes usando a biblioteca WordNet
6º. Tagging dos tokens usando a função nltk.pos_tag
7º. Obtenção da pontuação de cada token (positivo, negativo e objetividade) com a biblioteca SentiWordNet
8º. Cálculo de todas as pontuações recolhidas: Média das pontuações positivas - média das pontuações negativas
9º. Demonstração do resultado final em forma de gráfico com a biblioteca matplotlib

Observações:
1º. O diretório possui dois programas, sendo eles: projetoExplicativo.ipynb e blocoUnico.py. Ambos apresentam o mesmo código, entretanto o 'projetoExplicativo.ipynb' é dividido em blocos de códigos com a explicação e exemplificação de cada bloco para facilitar o entendimento de cada passo implementado.
