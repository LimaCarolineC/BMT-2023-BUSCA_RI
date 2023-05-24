import csv
import logging
import pandas as pd
import math
from nltk.stem import PorterStemmer

ps = PorterStemmer()

logging.basicConfig(filename="../LOG/indexador_log.log", level=logging.INFO, format="%(asctime)s - %(message)s")
logging.info("Indexador - Iniciando Execucao;")

path_config="../SRC/config/INDEX.CFG"

logging.info(f"Indexador - Lendo arquivo de configuracao: {path_config};")
index_cfg = open(path_config, 'r')
instrucoes = []

stemmer_option = False

logging.info(f"Obtendo informacoes do arquivo: {path_config};")
for line in index_cfg:
    if not("=" in line):
        if line.replace("\n","").replace(" ", "") == "STEMMER":
            stemmer_option = True
            logging.info("STEMMER OPTION ATIVADA!")
    else:
        split = line.replace("<","").rstrip(">\n ").split("=")
        instrucoes.append(split[1])

nome_arquivo, extensao = instrucoes[0].split(".")
nome_arquivo += "-STEMMER" if stemmer_option else "-NOSTEMMER"
leia = nome_arquivo + "." + extensao

logging.info(f"Arquivo a ser lido: {leia};")
logging.info(f"Arquivo para armazenar tf/idf: {instrucoes[1]};")
index_cfg.close()
logging.info(f"Leitura do arquivo {path_config} finalizada;")


logging.info(f"Iniciando leitura do arquivo {leia};")
path_leitura = "../RESULT/"+leia

lista_invertida_dic = {}
doc_total_termos = {}
palavra_info = {}

lista_invertida = pd.read_csv(path_leitura, sep=';', encoding="utf_8", header=None)
lista_invertida.columns = ['Words','ListDocs']
num_docs = 0

logging.info("Iniciando indexacao.")

for linha in lista_invertida.iterrows():
    documentos = linha[1]['ListDocs'].replace("[","").replace("]","").replace(" ","")
    documentos = documentos.split(",")
    last_doc = int(documentos[-1])
    num_docs = max(num_docs, last_doc)
    total_docs=0
    anterior=0
    for doc in documentos:
        if doc in doc_total_termos.keys():
           doc_total_termos[doc] = doc_total_termos[doc]+1
        else:
            doc_total_termos[doc] = 1

        if doc!=anterior:
            total_docs = total_docs+1
            anterior = doc

    palavra_info[linha[1]['Words']]=total_docs

logging.info(f"Numero total de documentos da colecao: {num_docs};")
logging.info("Iniciando calculo do TF/IDF de cada palavra.")

tfidf_dic = {}
imprime_csv = ["Word;W_ij\n"]

for linha in lista_invertida.iterrows():
    documentos = linha[1]['ListDocs'].replace("[","").replace("]","").replace(" ","")
    documentos = documentos.split(",")
    doc_anterior = documentos[0]
    num_termo_aparece = 0
    doc_em_analise = 0
    TF = 0
    IDF = 0
    TFIDF = 0

    for i in range(len(documentos)):

        if documentos[i]==doc_anterior:
            num_termo_aparece = num_termo_aparece + 1

            if i!=len(documentos)-1:
                if documentos[i+1]!=doc_anterior:
                    # TF = (n. de vezes que o termo aparece no doc)/(n. total de termos no doc
                    TF = (num_termo_aparece/doc_total_termos[doc_anterior])
                    #IDF = log(n. total de docs na colecao/ n. de docs q contêm o termo)
                    IDF = math.log((num_docs/palavra_info[linha[1]['Words']]))
                    #TF/IDF = TF*IDF
                    TFIDF = TF*IDF

                    #tfidf_dic[linha[1]['Words']] = TF * math.log(IDF)
                    if linha[1]['Words'] in tfidf_dic.keys():
                        tfidf_dic[linha[1]['Words']].append(doc_anterior + ": " + str(TFIDF))
                    else:
                        tfidf_dic[linha[1]['Words']] = [doc_anterior + ": " + str(TFIDF)]

                    doc_anterior = documentos[i+1]
                    num_termo_aparece = 0
            else:
                # TF = (n. de vezes que o termo aparece no doc)/(n. total de termos no doc
                TF = (num_termo_aparece / doc_total_termos[doc_anterior])
                # IDF = log(n. total de docs na colecao/ n. de docs q contém o termo)
                IDF = math.log((num_docs / palavra_info[linha[1]['Words']]))
                # TF/IDF = TF*IDF
                TFIDF = TF * IDF

                #tfidf_dic[linha[1]['Words']] = TF * math.log(IDF)
                if linha[1]['Words'] in tfidf_dic.keys():
                    tfidf_dic[linha[1]['Words']].append(doc_anterior + ": " + str(TFIDF))
                else:
                    tfidf_dic[linha[1]['Words']] = [doc_anterior + ": " + str(TFIDF)]

    imprime_csv.append(str(linha[1]['Words']) + ";" + str(tfidf_dic[linha[1]["Words"]]) + "\n")
    logging.info(f"Geracao do TF/IDF da palavra {linha[1]['Words']} finalizada;")

logging.info(f"Iniciando preenchimento do arquivo {instrucoes[1]};")
path_escreva = "../RESULT/"+instrucoes[1]
with open(path_escreva, 'w', newline='') as escreva_csv:
    escreva_csv.writelines(imprime_csv)

logging.info(f"Preenchimento do arquivo {instrucoes[1]} finalizada;")
logging.info("Indexador - Execucao Finalizada.")
