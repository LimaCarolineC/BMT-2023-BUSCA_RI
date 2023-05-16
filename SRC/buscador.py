import csv
import logging
import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import re
import numpy as np

stopwords_idioma = stopwords.words('english')
stopwords_idioma.extend(["et", "al"])

logging.basicConfig(filename="../LOG/buscador_log.log", level=logging.INFO, format="%(asctime)s - %(message)s")
logging.info("Buscador - Iniciando Execucao")

path_config = "../SRC/config/BUSCA.CFG"

logging.info(f"Buscador - Iniciando leitura do arquivo de configuracao: {path_config};")
busca_cf = open(path_config, 'r')
instrucoes = []

logging.info(f"Obtendo informacoes do arquivo: {path_config};")
for line in busca_cf:
    split = line.replace("<","").replace(">","").replace("\n","").split("=")
    instrucoes.append(split[1])
    logging.info(f"Leitura Instrucao {split[1]} ok;")

busca_cf.close()
logging.info(f"Obtencao as informacoes do arquivo: {path_config} finalizada;")

path_modelo = "../RESULT/"+instrucoes[0]
logging.info(f"Iniciando leitura do arquivo: {path_modelo};")
mv_dic = {}
mv_csv = pd.read_csv(path_modelo, sep=";", encoding="utf_8")
mv_csv.columns = ['Word','ListDocs']
last_doc = 0

logging.info(f"Tratando dados obtidos da {instrucoes[1]}")
for linha in mv_csv.iterrows():
    documentos = linha[1]['ListDocs'].replace("[","").replace("]","").replace(" ","").replace("'","")
    documentos = documentos.split(",")
    wij_list = {}
    for doc in documentos:
        pesos = doc.split(":")
        if int(pesos[0])>int(last_doc):
            last_doc = pesos[0]

        #wij[doc] = wij
        wij_list[pesos[0]] = pesos[1]

    # wij_list[docj] = [wij]
    mv_dic[str([linha[1]['Word']]).replace("[","").replace("]","").replace(" ","").replace("'","")] = wij_list
logging.info(f"Leitura do arquivo: {path_modelo} finalizada;")


path_consultas = "../RESULT/"+instrucoes[1]
logging.info(f"Iniciando leitura do arquivo: {path_consultas};")

query_list_dic = {}

consultas_csv = pd.read_csv(path_consultas, sep=";", encoding= "utf_8")
consultas_csv.columns = ['QueryNumber', 'QueryText']

logging.info(f"Tratando dados obtidos da {instrucoes[1]}")
for linha in consultas_csv.iterrows():
    query_texts = re.sub("[^a-zA-Z]+", " ",linha[1]['QueryText'])
    query_texts = re.sub(r"[^\w\s]", "", query_texts)
    query_texts_limpa = nltk.word_tokenize(query_texts)
    palavras = []
    for word in query_texts_limpa:
        if word.lower() not in stopwords_idioma and len(word.lower())>=2:
            palavras.append(word.upper())

    query_list_dic[linha[1]['QueryNumber']] = palavras
logging.info(f"Leitura do arquivo: {path_consultas} finalizada;")

logging.info("Iniciando calculo de similaridade;")

imprime = ["QueryNumber;Ranking;Doc;Similaridade\n"]

for query_number in query_list_dic.keys():
    query_list_result_dic = {}
    for i in range(int(last_doc)):
        num_doc = str(i+1)
        vet_mv = []
        vet_query = []
        for palavra in query_list_dic[query_number]:
            if mv_dic.get(palavra) is None or mv_dic[palavra].get(num_doc) is None:
                vet_mv.append(0)
                vet_query.append(1)
            else:
                vet_mv.append(float(mv_dic[palavra].get(num_doc)))
                vet_query.append(1)

        produto_interno = np.dot(vet_query, vet_mv)
        norma = np.linalg.norm(vet_mv)*np.linalg.norm(vet_query)
        if norma == 0:
            similaridade = 0
        else:
            similaridade = produto_interno/norma

        query_list_result_dic[str(query_number)+ ";ranking;"+str(num_doc)] = similaridade

    query_list_result_dic = sorted(query_list_result_dic.items(), key=lambda x: x[1], reverse=True)
    cont = 1;
    for chave in query_list_result_dic:
        inicio = chave[0].split(";")
        imprime.append(
            inicio[0] + ";" + inicio[1].replace("ranking", str(cont)) + ";" + inicio[2] + ";" + str(chave[1]) + "\n")
        cont = cont + 1

logging.info("Calculo de similaridade finalizado;")

logging.info(f"Iniciando criacao do arquivo {instrucoes[2]};")

path_resultados = "../RESULT/"+instrucoes[2]
with open(path_resultados, 'w', newline='') as escreva_csv:
    escreva_csv.writelines(imprime)

logging.info(f"Criacao do arquivo {path_resultados} finalizada;")
logging.info("Buscador - Exacucao Finalizada")
